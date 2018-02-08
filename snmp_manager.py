import socket, struct
from pysnmp.hlapi import *
from pymongo import MongoClient
from pprint import pprint


def main():
    db = create_db_connection()
    address = get_def_gateway()
    # address = '10.0.90.1'
    eng = create_snmp_engine()
    ip_list, mac_list = get_arp_table(eng, address)
    oid_list = ['1.0.8802.1.1.2.1.3.6', '1.0.8802.1.1.2.1.3.3']
    get_details(eng, ip_list, mac_list, oid_list, db)
    used_ips = [address]
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
    routers = db.snmp_table.find({"cap_isRouter": 1}, {"ip_addr": 1})
    for document in routers:
        pprint(document)
    return routers


def add_to_db(db, list):
    if db.snmp_table.find_one({'hostname': list[10]}, {"hostname": 1}) is None:
        db.snmp_table.insert({'ip_addr': list[0],
                              'mac_addr': list[1],
                              'cap_isOther': list[2],
                              'cap_isRepeater': list[3],
                              'cap_isBridge': list[4],
                              'cap_isWlanAP': list[5],
                              'cap_isRouter': list[6],
                              'cap_isTelephone': list[7],
                              'cap_isDocsisCableDevice': list[8],
                              'cap_isStationOnly': list[9],
                              'hostname': list[10]})
    else:
        db.snmp_table.update({'hostname': list[10]},
                             {'$addToSet': {'ip_addr': { '$each': list[0]}, 'mac_addr': {'$each': list[1]}}},
                             upsert=True)


def get_details(eng, ip_list, mac_list, oid_list, db):
    for ip in ip_list:
        mac = mac_list[ip_list.index(ip)]
        print("The current IP is: " + ip)
        details = [[ip], [mac]]
        snmp_details(eng, oid_list, details, ip, db)


def snmp_details(eng, oid_list, details, ip, db):
    for oid in oid_list:
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(eng,
                                                                            CommunityData('capstone-ro'),
                                                                            UdpTransportTarget((ip, 161)),
                                                                            ContextData(),
                                                                            ObjectType(ObjectIdentity(oid))):
            if errorIndication:
                print(errorIndication)
                return
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                details = parse_details(varBinds, details)
                break
    add_to_db(db, details)


def parse_details(varBinds, details):
    name, value = varBinds[0]
    if str(name) == '1.0.8802.1.1.2.1.3.6.0':
        a = bin(int.from_bytes(str(value).encode(), 'big'))
        caps = check_capabilities(a)
        details.extend(caps)
    elif str(name) == '1.0.8802.1.1.2.1.3.3.0':
        hostname = str(value)
        details.append(hostname)
    return details


def check_capabilities(binary):
    binary = binary[2:-8]
    chars = list(binary.zfill(8))
    return chars


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
               CommunityData('capstone-ro'),
               UdpTransportTarget((address, 161)),
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
