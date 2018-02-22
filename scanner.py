import socket
import pcapy
import sys
import datetime
from struct import *
from pcap_scanner_app import packet
from pymongo import MongoClient


def main(argv):
    devices = pcapy.findalldevs()
    # print(devices)
    # print("Available devices are: ")
    # for d in devices:
        # print(d)

    # dev = input("Enter device name to sniff: ")
    dev = 'tap0'
    # print("Sniffing device " + dev)
    """
    open device
    # Arguments here are:
    #   device
    #   snaplen (maximum number of bytes to capture _per_packet_)
    #   promiscuous mode (1 for true)
    #   timeout (in milliseconds)
    """
    f = open('/home/brian/Desktop/test.txt', 'w')
    f.write(str(datetime.datetime.now()))
    f.close()
    cap = pcapy.open_live(dev, 65536, 1, 0)
    # Start sniffing packets
    while 1:
        (header, packet) = cap.next()
        parse_packet(packet)


def connect_db(packet):
    client = MongoClient()
    db = client.ntm_db
    new_packet = [{'mac_addr': packet.mac, 'hostname': packet.system_name, 'ip_addr': packet.mgmt_addr}]
    db.ntm_table.insert(new_packet)
    # db.ntm_table.create_index([("mac", pymongo.ASCENDING)],
    #                           unique=True)


def eth_addr(a):
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (a[0], a[1], a[2], a[3], a[4], a[5])
    return b


def format_hex(original):
    if isinstance(original, bytes):
        original = int.from_bytes(original, byteorder='little', signed=False)
    list_var = [original]
    a = ''.join('{:02x}'.format(a) for a in list_var)
    return a


def parse_packet(packet):
    eth_header_length = 14
    eth_header = packet[:eth_header_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = eth[2]
    destination_addr = eth_addr(packet[0:6])
    if destination_addr == '01:00:0c:cc:cc:cc':
        source_addr = eth_addr(packet[6:12])
        print('Destination MAC: ' + destination_addr + ' Source MAC: ' + source_addr + ' Length: ' + str(eth_protocol))
        parse_cdp_packet(packet, eth_header_length, source_addr)
    elif destination_addr == '01:80:c2:00:00:0e':
        source_addr = eth_addr(packet[6:12])
        print('Destination MAC: ' + destination_addr + ' Source MAC: ' + source_addr + ' Protocol: ' + str(eth_protocol))
        parse_lldp_packet(packet, eth_header_length, source_addr)


def parse_lldp_packet(packet, eth_length, src_mac):
    print("LLDP")
    begin_lldp_data = packet[eth_length:]
    check_bytes(begin_lldp_data, src_mac)


def parse_cdp_packet(packet, eth_length, src_mac):
    print("CDP")
    llc_header_length = 8
    begin_cdp_data = packet[eth_length+llc_header_length:]
    check_cdp_bytes(begin_cdp_data, src_mac)


def check_cdp_bytes(bytes_var, src_mac):
    first = 4
    second = first+1
    cdp_overhead = 4
    cdp_header = unpack('!BB', bytes_var[0:2])
    version = str(cdp_header[0])
    if version != '2':
        return
    ttl = str(cdp_header[1])
    # print('CDP Version: ' + version + ' TTL: ' + ttl)
    while second < len(bytes_var):
        var = unpack('!HH', bytes_var[first:second+3])
        tlv_type = var[0]
        tlv_length = var[1]
        if second >= len(bytes_var):
            # print("End of Packet")
            break
        if int(tlv_type) == 1:
            sys_name = parse_system_name(bytes_var[first+cdp_overhead:first+tlv_length])
            first += tlv_length
            second += tlv_length
        # elif int(tlv_type) == 2:
        #     first += tlv_length
        #     second += tlv_length
        elif int(tlv_type) == 3:
            port_desc = parse_port_desc(bytes_var[first+cdp_overhead:first+tlv_length])
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 4:
            cap = parse_cdp_capabilities(bytes_var[first:first+tlv_length])
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 5:
            sys_desc = parse_system_description(bytes_var[first+cdp_overhead:first+tlv_length])
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 6:
            parse_platform(bytes_var[first+cdp_overhead:first+tlv_length])
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 7:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 8:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 9:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 10:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 11:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 18:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 19:
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 22 or int(tlv_type) == 2:
            mgmt_addr = parse_cdp_manage_add(bytes_var[first:first+tlv_length])
            first += tlv_length
            second += tlv_length
        elif int(tlv_type) == 26:
            first += tlv_length
            second += tlv_length
        else:
            second = len(bytes_var)
    # p = models.Device.create(ttl, src_mac, sys_name, sys_desc, port_desc, cap, mgmt_addr)
    # p.save()
    # invalid_device = models.Device.objects.get(expire__lt=datetime.datetime.now())
    # invalid_device.save()
    p = packet.Packet(src_mac, sys_name, mgmt_addr)
    connect_db(p)
    # print('CDP Packet Created')


def check_bytes(bytes_var, src_mac):
    first = 0
    second = first+1
    tlv_overhead = 2
    tlv_type_len = 7
    tlv_len_len = 9
    while second < len(bytes_var):
        var = unpack('!H', bytes_var[first:second+1])
        var_bin = (bin(int(format_hex(var[0]), 16))[2:].zfill(16))
        sys_name = ''
        mgmt_addr = ''
        tlv_type = var_bin[0:tlv_type_len]
        tlv_length = var_bin[-tlv_len_len:]
        tlv_length = int(tlv_length, 2)
        if second >= len(bytes_var):
            # print("End of Packet")
            break
        if int(tlv_type, 2) == 1:
            parse_chassis_id(bytes_var[first:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 2:
            parse_port_id(bytes_var[first:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 3:
            ttl = parse_ttl(bytes_var[first:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 4:
            port_desc = parse_port_desc(bytes_var[first+tlv_overhead:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 5:
            sys_name = parse_system_name(bytes_var[first+tlv_overhead:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 6:
            sys_desc = parse_system_description(bytes_var[first+tlv_overhead:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 7:
            cap = parse_capabilities(bytes_var[first:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 8:
            mgmt_addr = parse_manage_add(bytes_var[first:first+tlv_overhead+tlv_length])
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 127:
            first += tlv_overhead+tlv_length
            second += tlv_overhead + tlv_length
        elif int(tlv_type, 2) == 0:
            # p = models.Device.create(ttl, src_mac, sys_name, sys_desc, port_desc, cap, mgmt_addr)
            # p.save()
            # invalid_device = models.Device.objects.get(expire__lt=datetime.datetime.now())
            # invalid_device.save()
            p = packet.Packet(src_mac, sys_name, mgmt_addr)
            connect_db(p)
            # print('LLDP Packet Created')
            break


def parse_platform(bytestring):
    platform = bytestring.decode("utf-8")
    # print('Platform: ' + platform)


def parse_chassis_id(bytestring):
    var = unpack('!HB6s', bytestring)
    chassis_id = eth_addr(var[2])
    # print('Chassis ID: ' + chassis_id)


def parse_port_id(bytestring):
    var = unpack('!HB6s', bytestring)
    port_id = var[2].decode("utf-8")
    # print('Originating Port ID: ' + port_id)


def parse_ttl(bytestring):
    var = unpack('!HH', bytestring)
    ttl = str(var[1])
    # print('TTL: ' + ttl)
    return ttl


def parse_system_name(bytestring):
    sys_name = bytestring.decode("utf-8")
    # print('System Name: ' + sys_name)
    return sys_name


def parse_system_description(bytestring):
    sys_desc = bytestring.decode("utf-8")
    # print('System Description: ' + sys_desc)
    return sys_desc


def parse_port_desc(bytestring):
    port_desc = bytestring.decode("utf-8")
    # print('Originating Port Description: ' + port_desc)
    return port_desc


def parse_capabilities(bytestring):
    var = unpack('!HHH', bytestring)
    cap_bin = (bin(int(format_hex(var[1]), 16))[2:].zfill(16))
    # print("Capabilities: ")
    determine_capabilities(cap_bin)
    en_cap_bin = (bin(int(format_hex(var[2]), 16))[2:].zfill(16))
    # print("Enabled Capabilities: ")
    cap = determine_capabilities(en_cap_bin)
    return cap


def parse_cdp_capabilities(bytestring):
    var = unpack('!HHI', bytestring)
    cap_bin = (bin(int(format_hex(var[2]), 16))[2:].zfill(32))
    device = ''
    if cap_bin[-1] == '1' and cap_bin[-4] == '1':
        device = "ml_switch"
    elif cap_bin[-4] == '1':
        device = "switch"
    elif cap_bin[-1] == '1':
        device = "router"
    return device
    # print("Enabled Capabilities: ")


def determine_cdp_capabilities(binarystring):
    cap_list = []
    if int(binarystring[-1]) == 1:
        # print("\tRouter: Capable")
        cap_list.append("Router: Capable")
    if int(binarystring[-2]) == 1:
        # print("\tTransparent Bridge/Switch: Capable")
        cap_list.append("Transparent Bridge/Switch: Capable")
    if int(binarystring[-3]) == 1:
        # print("\tSource Route Bridge/Switch: Capable")
        cap_list.append("Source Route Bridge/Switch: Capable")
    if int(binarystring[-4]) == 1:
        # print("\tSwitch: Capable")
        cap_list.append("Switch: Capable")
    if int(binarystring[-5]) == 1:
        # print("\tHost: Capable")
        cap_list.append("Host: Capable")
    if int(binarystring[-6]) == 1:
        # print("\tIGMP: Capable")
        cap_list.append("IGMP: Capable")
    if int(binarystring[-7]) == 1:
        # print("\tRepeater: Capable")
        cap_list.append("Repeater: Capable")
    cap_list.append('')
    return cap_list


def determine_capabilities(binarystring):
    cap_list = []
    if int(binarystring[-1]) == 1:
        # print("\tOther: Capable")
        cap_list.append("Other: Capable")
    if int(binarystring[-2]) == 1:
        # print("\tRepeater: Capable")
        cap_list.append("Repeater: Capable")
    if int(binarystring[-3]) == 1:
        # print("\tBridge/Switch: Capable")
        cap_list.append("Bridge/Switch: Capable")
    if int(binarystring[-4]) == 1:
        # print("\tWAP: Capable")
        cap_list.append("WAP: Capable")
    if int(binarystring[-5]) == 1:
        # print("\tRouter: Capable")
        cap_list.append("Router: Capable")
    if int(binarystring[-6]) == 1:
        # print("\tTelephone: Capable")
        cap_list.append("Telephone: Capable")
    if int(binarystring[-7]) == 1:
        # print("\tDOCSIS device: Capable")
        cap_list.append("DOCSIS: Capable")
    if int(binarystring[-8]) == 1:
        # print("\tStation Only: Capable")
        cap_list.append("Station Only: Capable")
    return cap_list


def parse_manage_add(bytestring):
    var = unpack('!HBB4sBIB', bytestring)
    addr_type = var[2]
    if addr_type == 1:
        addr = socket.inet_ntop(socket.AF_INET, var[3])
    else:
        addr = socket.inet_ntop(socket.AF_INET6, var[3])
    # print('Management Address: ' + addr)
    return addr


def parse_cdp_manage_add(bytestring):
    var = unpack('!HHIBBBH4s', bytestring)
    addr_type = format_hex(var[5])
    if addr_type == 'cc':
        addr = socket.inet_ntop(socket.AF_INET, var[7])
    else:
        addr = socket.inet_ntop(socket.AF_INET6, var[7])
    # print('Management Address: ' + addr)
    return addr


if __name__ == "__main__":
    main(sys.argv)
