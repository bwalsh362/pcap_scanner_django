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
        return render(request, 'topology.html', {'device_list': device_list})


class InventoryPageView(ListView):
    def get(self, request, **kwargs):
        return render(request, 'inventory.html', context=None)