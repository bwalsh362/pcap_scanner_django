from django.shortcuts import render
from django.views.generic import TemplateView, ListView


# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)


class TopologyPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'topology.html', context=None)


class InventoryPageView(ListView):
    def get(self, request, **kwargs):
        return render(request, 'inventory.html', context=None)