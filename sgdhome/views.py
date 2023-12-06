from django.shortcuts import render
from . import mqtt

# Create your views here.
from django.views.generic.base import TemplateView

class HomePageViews(TemplateView):
    template_name = 'index.html'
    

# запуск mqtt
# mqtt.client.loop_start()
