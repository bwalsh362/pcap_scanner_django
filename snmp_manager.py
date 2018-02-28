import socket, struct
from pysnmp.hlapi import *
from pymongo import MongoClient
import alert
import sys
used_ips = []


def main():
    print(sys.argv)
    db = create_db_connection()
    # address = get_def_gateway()
    address = '10.0.10.1'
    eng = create_snmp_engine()
    ip_list, mac_list = get_arp_table(eng, address)
    oid_list = ['1.0.8802.1.1.2.1.3.3.0', '1.0.8802.1.1.2.1.3.6.0']
    get_details(eng, ip_list, mac_list, oid_list, db)
    used_ips.append(address)
    router_list = get_router_ips(db)
    for ip in router_list:
        if ip not in used_ips:
            ip_list, mac_list = get_arp_table(eng, ip)
            get_details(eng, ip_list, mac_list, oid_list, db)


def create_db_connection():
    client = MongoClient()
    db = client.ntm_db
    return db


def get_router_ips(db):
    routers = db.snmp_table.find({"type": 'router'}, {"ip_addr": 1, "_id": 0})
    ip_list = []
    for document in routers:
        doc_list = list(document.values())
        ip_list.extend(doc_list[0])
    return ip_list


def add_to_db(db, packet_list):
    if packet_list.__len__() >= 5:
        if db.snmp_table.find_one({'hostname': packet_list[2]}, {"hostname": 1}) is None:
            alert.send_alert("WARNING!!! A new device with the following information was added."
                             "\n\tHostname: " + str(packet_list[2]) + "\n"
                             "\tIP Address(s): " + str(packet_list[0]) + "\n"
                             "If this was expected, ignore this message.")
            db.snmp_table.insert({'ip_addr': packet_list[0],
                                  'mac_addr': packet_list[1],
                                  'type': packet_list[3],
                                  'hostname': packet_list[2],
                                  'conn_devices': packet_list[4],
                                  'interface_details': packet_list[5],
                                  'device_details': packet_list[6],
                                  'duplex_details': packet_list[7]})
        else:
            prev_int_details = db.snmp_table.find_one({'hostname': packet_list[2]}, {'_id': 0, 'interface_details': 1})
            details_list = list(prev_int_details.values())
            bandwidth_arr = []
            if sys.argv[4] == "True":
                prev_interface_input = []
                interface_speed = []
                for interface in details_list[0]:
                    prev_interface_input.append(interface[4])
                    interface_speed.append(interface[2])
                bandwidth_arr = calculate_bandwidth(prev_interface_input, interface_speed, packet_list[5], sys.argv[3])
            db.snmp_table.update({'hostname': packet_list[2]},
                                 {'$addToSet': {'ip_addr': {'$each': packet_list[0]}, 'mac_addr': {'$each': packet_list[1]}, 'conn_devices': {'$each': packet_list[4]}}, '$set': {'interface_details': packet_list[5], 'bandwidth_util': bandwidth_arr}},
                                 upsert=True)


def calculate_bandwidth(prev_interface_input, interface_speed, new_interface_details_arr, time):
    bandwidth_list = []
    for interface in range(prev_interface_input.__len__()):
        first_equation = (abs(int(prev_interface_input[int(interface)]) - int(new_interface_details_arr[int(interface)][4])) * 8 * 100)
        second_equation = (int(time) * int(interface_speed[int(interface)]))
        bandwidth = (int(first_equation)/int(second_equation))
        bandwidth = round(bandwidth, 2)
        bandwidth_list.append(bandwidth)
    return bandwidth_list


def get_details(eng, ip_list, mac_list, oid_list, db):
    for ip in ip_list:
        print("Checking IP: " + ip)
        mac = mac_list[ip_list.index(ip)]
        details = [[ip], [mac]]
        snmp_details(eng, oid_list, details, ip, mac, db)
        conn_devices = snmp_walk_details(eng, '1.0.8802.1.1.2.1.4.1.1.9', ip)
        if conn_devices is not None and conn_devices.__len__() >= 1:
            details.append(conn_devices)
        interface_details = snmp_walk_details(eng, '1.3.6.1.2.1.2.2', ip)
        if interface_details is not None and interface_details.__len__() >= 1:
            details.append(interface_details)
        device_details = snmp_walk_details(eng, '1.3.6.1.2.1.47.1.1.1', ip)
        if device_details is not None and device_details.__len__() >= 1:
            details.append(device_details)
        else:
            details.append([""])
        duplex_details = snmp_walk_details(eng, '1.3.6.1.2.1.10.7.2.1.19', ip)
        if duplex_details is not None and duplex_details.__len__() >= 1:
            details.append(duplex_details)
        add_to_db(db, details)


def snmp_details(eng, oid_list, details, ip, mac, db):
    for oid in oid_list:
        g = getCmd(eng,
                   CommunityData(sys.argv[2]),
                   UdpTransportTarget((ip, sys.argv[1])),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        results = (next(g))[3]
        if len(results) == 0:
            print("No SNMP response")
            return
        results_value = results[0][1]
        if str(results_value) == "":
            print("OID does not exist on device")
            snmp_details(eng, ['1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.7.0'], details, ip, mac, db)
            conn_devices = snmp_walk_details(eng, '1.3.6.1.4.1.9.9.23.1.2.1.1.6', ip)
            details.append(conn_devices)
            return
        else:
            details = parse_details(results, details)
    # add_to_db(db, details)


def snmp_walk_details(eng, oid, ip):
    details = []
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(eng,
                                                                        CommunityData(sys.argv[2]),
                                                                        UdpTransportTarget((ip, sys.argv[1])),
                                                                        ContextData(),
                                                                        ObjectType(ObjectIdentity(oid)),
                                                                        lexicographicMode=False):
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                if oid == '1.3.6.1.4.1.9.9.23.1.2.1.1.6' or oid == '1.0.8802.1.1.2.1.4.1.1.9':
                    details = parse_conn_device_details(varBinds, details)
                elif oid == '1.3.6.1.2.1.2.2':
                    details = parse_interface_details(varBinds, details)
                elif oid == '1.3.6.1.2.1.47.1.1.1':
                    details = parse_device_details(varBinds, details)
                elif oid == '1.3.6.1.2.1.10.7.2.1.19':
                    details = parse_duplex_details(varBinds, details)
    return details


def parse_duplex_details(varBinds, details):
    name, value = varBinds[0]
    if value == 2:
        details.append("HALF-DUPLEX")
    elif value == 3:
        details.append("FULL-DUPLEX")
    else:
        details.append("UNKNOWN")
    return details


def parse_device_details(varBinds, details):
    name, value = varBinds[0]
    if str(name) == '1.3.6.1.2.1.47.1.1.1.1.2.1':
        details.append(str(value))
    elif str(name) == '1.3.6.1.2.1.47.1.1.1.1.11.1':
        details.append(str(value))
    elif str(name) == '1.3.6.1.2.1.47.1.1.1.1.12.1':
        details.append(str(value))
    elif str(name) == '1.3.6.1.2.1.47.1.1.1.1.13.1':
        details.append(str(value))
    return details


def parse_interface_details(varBinds, details):
    name, value = varBinds[0]
    if str(name)[:20] == '1.3.6.1.2.1.2.2.1.1.':
        details.append([str(value)])
    elif str(name)[:20] == '1.3.6.1.2.1.2.2.1.2.':
        for item in details:
            if item[0] == str(name).split('.')[-1]:
                item.append(str(value))
    elif str(name)[:20] == '1.3.6.1.2.1.2.2.1.5.':
        for item in details:
            if item[0] == str(name).split('.')[-1]:
                item.append(str(value))
    elif str(name)[:20] == '1.3.6.1.2.1.2.2.1.8.':
        for item in details:
            if item[0] == str(name).split('.')[-1]:
                item.append(str(value))
    elif str(name)[:20] == '1.3.6.1.2.1.2.2.1.10':
        for item in details:
            if item[0] == str(name).split('.')[-1]:
                item.append(str(value))
    return details


def parse_conn_device_details(varBinds, details):
    name, value = varBinds[0]
    if str(name)[:24] == '1.0.8802.1.1.2.1.4.1.1.9':
        details.append(str(value))
        print("LLDP Connected Devices: " + value)
    elif str(name)[:28] == '1.3.6.1.4.1.9.9.23.1.2.1.1.6':
        details.append(str(value))
        print("CDP Connected Devices: " + value)
    return details


def parse_details(varBinds, details):
    name, value = varBinds[0]
    if str(name) == '1.0.8802.1.1.2.1.3.6.0':
        a = bin(int.from_bytes(str(value).encode(), 'big'))
        caps = check_capabilities(a)
        details.append(caps)
    elif str(name) == '1.3.6.1.2.1.1.7.0':
        caps = check_neutral_caps(value)
        details.append(caps)
    elif str(name) == '1.0.8802.1.1.2.1.3.3.0' or str(name) == '1.3.6.1.2.1.1.5.0':
        hostname = str(value)
        details.append(hostname)
    return details


def check_neutral_caps(value):
    str_value = str(value)
    device = ''
    if str_value == "6":
        device = "switch"
    elif str_value == "78":
        device = "router"
    return device


def check_capabilities(binary):
    binary = binary[2:-8]
    chars = list(binary.zfill(8))
    device = ''
    if chars[4] == '1' and chars[6] == '1':
        device = "ml_switch"
    elif chars[4] == '1':
        device = "switch"
    elif chars[6] == '1':
        device = "router"
    return device


def get_def_gateway():
    """Read the default gateway directly from /proc (linux only)"""
    with open("/proc/net/route") as file:
        for line in file:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def get_arp_table(engine, address):
    ip_list = []
    mac_list = []
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(engine,
               CommunityData(sys.argv[2]),
               UdpTransportTarget((address, sys.argv[1])),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.3.1.1.2'))):
        name, value = varBinds[0]
        oid = str(name)[:19]
        if oid != '1.3.6.1.2.1.3.1.1.2' and oid != '1.3.6.1.2.1.3.1.1.3':
            break
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBinds in varBinds:
                split_str = str(varBinds).split(' = ')[1]
                if oid == '1.3.6.1.2.1.3.1.1.2':
                    split_str = split_str[2:]
                    split_str = [split_str[i:i+2] for i in range(0, len(split_str), 2)]
                    split_str = ':'.join(split_str)
                    mac_list.append(split_str)
                elif oid == '1.3.6.1.2.1.3.1.1.3':
                    ip_list.append(split_str)
    return ip_list, mac_list


def create_snmp_engine():
    snmp_eng = SnmpEngine()
    return snmp_eng


if __name__ == "__main__":
    main()
