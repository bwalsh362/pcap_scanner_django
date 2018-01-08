class Packet:
    # ttl = 0
    # mac = ''
    # system_name = ''
    # system_desc = ''
    # org_port = ''
    # capabilities = ''
    # mgmt_addr = ''

    def __init__(self, ttl, mac, sys_name, sys_desc, org_port, cap, mgmt_addr):
        self.ttl = ttl
        self.mac = mac
        self.system_name = sys_name
        self.system_desc = sys_desc
        self.org_port = org_port
        self.capabilities = cap
        self.mgmt_addr = mgmt_addr
