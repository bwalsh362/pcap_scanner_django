from django.db import models


# Create your models here.
class Device(models.Model):
    expire = models.DateTimeField
    mac = models.CharField(primary_key=True, max_length=20)
    sys_name = models.CharField(max_length=50)
    sys_desc = models.CharField(max_length=300)
    org_port = models.CharField(max_length=40)
    capabilities = models.CharField(max_length=500)
    mgmt_addr = models.CharField(max_length=15)

    @classmethod
    def create(cls, ttl, mac, sys_name, sys_desc, org_port, cap, mgmt_addr):
        import datetime
        expire = datetime.datetime.now() + datetime.timedelta(0, ttl)
        device = cls(expire=expire, mac=mac, sys_name=sys_name, sys_desc=sys_desc, org_port=org_port, cap=cap, mgmt_addr=mgmt_addr)
        return device

    def __str__(self):
        return self.sys_name
