from django.contrib import admin
from django.urls import path, re_path
from pcap_scanner_app.views import HomePageView, TopologyPageView, InventoryPageView, DevicePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('topology/', TopologyPageView.as_view(), name='topology'),
    path('inventory/', InventoryPageView.as_view(), name='inventory'),
    re_path(r'^inventory/tag=(?P<tag>[0-9A-Za-z.-]+)/$', DevicePageView.as_view(), name='device'),
]