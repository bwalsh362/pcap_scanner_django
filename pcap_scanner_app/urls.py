from django.contrib import admin
from django.urls import path
from pcap_scanner_app.views import HomePageView, TopologyPageView, InventoryPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('topology/', TopologyPageView.as_view(), name='topology'),
    path('inventory/', InventoryPageView.as_view(), name='inventory'),
]