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
        devices = db.snmp_table.find()
        return render(request, 'topology.html', {'device_list': devices}, content_type=list)


class InventoryPageView(ListView):
    def get(self, request, **kwargs):
        client = MongoClient()
        db = client.ntm_db
        details = db.snmp_table.find({}, {'_id': 0, 'hostname': 1, 'ip_addr': 1, 'mac_addr': 1})
        return render(request, 'inventory.html', {'details_list': details})
