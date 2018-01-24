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
        details = c.execute('''SELECT ip_addr AS 'IP Address', 
                                mac_addr AS 'MAC Address',
                                CASE WHEN cap_isOther = 1 then 'True' WHEN cap_isOther = 0 then 'False' else 'NN' END AS 'Other',
                                CASE WHEN cap_isRepeater = 1 then 'True' WHEN cap_isRepeater = 0 then 'False' else 'NN' END AS 'Repeater',
                                CASE WHEN cap_isBridge = 1 then 'True' WHEN cap_isBridge = 0 then 'False' else 'NN' END AS 'Swich',
                                CASE WHEN cap_isWlanAP = 1 then 'True' WHEN cap_isWlanAP = 0 then 'False' else 'NN' END AS 'WAP',
                                CASE WHEN cap_isRouter = 1 then 'True' WHEN cap_isRouter = 0 then 'False' else 'NN' END AS 'Router',
                                CASE WHEN cap_isTelephone = 1 then 'True' WHEN cap_isTelephone = 0 then 'False' else 'NN' END AS 'Telephone',
                                CASE WHEN cap_isDocsisCableDevice = 1 then 'True' WHEN cap_isDocsisCableDevice = 0 then 'False' else 'NN' END AS 'DOCSIS Device',
                                CASE WHEN cap_isStationOnly = 1 then 'True' WHEN cap_isStationOnly = 0 then 'False' else 'NN' END AS 'Station Only',
                                hostname AS 'Hostname'
                                FROM snmp_data''')
        details_list = details.fetchall()
        column_names = list(map(lambda x: x[0], c.description))
        conn.close()
        return render(request, 'inventory.html', {'details_list': details_list, 'column_names': column_names})
