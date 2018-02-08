import socket, struct
import sqlite3
from pysnmp.hlapi import *
from pymongo import MongoClient


def main():
    cursor, connection = create_db_connection()
    check_table(cursor, '''SELECT * FROM sqlite_master WHERE type='table' AND name='snmp_data';''')
    address = get_def_gateway()
    eng = create_snmp_engine()
    ip_list, mac_list = get_arp_table(eng, address)
    oid_list = ['1.0.8802.1.1.2.1.3.6', '1.0.8802.1.1.2.1.3.3']
    get_details(eng, ip_list, mac_list, oid_list, cursor, connection)
    used_ips = [address]
    router_list = get_router_ips(cursor)
    for ip in router_list:
        if ip not in used_ips:
            ip_list, mac_list = get_arp_table(eng, ip)
            get_details(eng, ip_list, mac_list, oid_list, cursor, connection)


def create_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return c, conn


def check_table(cursor, query):
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        create_snmpdata_table(cursor)


def get_router_ips(cursor):
    routers = cursor.execute('''SELECT ip_addr FROM snmp_data WHERE cap_isRouter = 1''')
    routers_list = routers.fetchall()
    return routers_list


def add_to_db(cursor, list, connection):
    print(list)
    cursor.execute('''INSERT OR IGNORE INTO snmp_data(ip_addr, 
                                mac_addr, 
                                cap_isOther, 
                                cap_isRepeater, 
                                cap_isBridge, 
                                cap_isWlanAP, 
                                cap_isRouter, 
                                cap_isTelephone, 
                                cap_isDocsisCableDevice, 
                                cap_isStationOnly, 
                                hostname) 
                                VALUES(?,?,?,?,?,?,?,?,?,?,?);''', list)
    connection.commit()


def create_snmpdata_table(cursor):
    cursor.execute('''CREATE TABLE snmp_data (  ip_addr text NOT NULL, 
                                                mac_addr text NOT NULL,
                                                cap_isOther INTEGER,
                                                cap_isRepeater INTEGER,
                                                cap_isBridge INTEGER,
                                                cap_isWlanAP INTEGER,
                                                cap_isRouter INTEGER,
                                                cap_isTelephone INTEGER,
                                                cap_isDocsisCableDevice INTEGER,
                                                cap_isStationOnly INTEGER,
                                                hostname text NOT NULL,
                                                PRIMARY KEY (ip_addr, mac_addr, hostname));''')


def get_details(eng, ip_list, mac_list, oid_list, cursor, connection):
    for ip in ip_list:
        mac = mac_list[ip_list.index(ip)]
        print("The current IP is: " + ip)
        details = [ip, mac]
        snmp_details(eng, oid_list, details, ip, cursor, connection)


def snmp_details(eng, oid_list, details, ip, cursor, connection):
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
    add_to_db(cursor, details, connection)


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
