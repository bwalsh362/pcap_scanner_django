from django.shortcuts import render
from django.views.generic import TemplateView, ListView
import sqlite3


# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)


class TopologyPageView(TemplateView):
    def get(self, request, **kwargs):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        devices = c.execute('SELECT * FROM packets')
        device_list = devices.fetchall()
        conn.close()
        return render(request, 'topology.html', {'device_list': device_list})


class InventoryPageView(ListView):
    def get(self, request, **kwargs):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        details = c.execute('SELECT * FROM snmp_data')
        details_list = details.fetchall()
        column_names = list(map(lambda x: x[0], c.description))
        conn.close()
        details_list.insert(0, column_names)
        return render(request, 'inventory.html', {'details_list': details_list})