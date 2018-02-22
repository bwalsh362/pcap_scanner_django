from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from pymongo import MongoClient
# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)


class TopologyPageView(TemplateView):
    def get(self, request, **kwargs):
        client = MongoClient()
        db = client.ntm_db
        devices = db.snmp_table.find({}, {'_id': 0})
        devices_arr = []
        for document in devices:
            device_list = list(document.values())
            devices_arr.append(device_list)
        return render(request, 'topology.html', {'device_list': devices_arr})


class InventoryPageView(ListView):
    def get(self, request, **kwargs):
        client = MongoClient()
        db = client.ntm_db
        details = db.snmp_table.find({}, {'_id': 0, 'hostname': 1, 'ip_addr': 1, 'mac_addr': 1, 'conn_devices': 1, 'interface_details': 1, 'device_details': 1})
        details_arr = []
        for document in details:
            details_list = list(document.values())
            details_arr.append(details_list)
        return render(request, 'inventory.html', {'details_list': details_arr})
