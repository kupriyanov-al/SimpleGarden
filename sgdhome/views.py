import datetime

from django.shortcuts import get_object_or_404, render
from . import mqtt
from .models import DBTelemetry
from .serializers import DBTelemetrySerializer

# Create your views here.
from django.views.generic.base import TemplateView
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response


class HomePageViews(TemplateView):
    template_name = 'index.html'
 

#  REST API
class DBTelemetryListView(generics.ListAPIView):
    # queryset = DBTelemetry.objects.all()[:10]
    serializer_class = serializers.DBTelemetrySerializer



    def get_queryset(self):
        # выводим из БД данные за сутки
        dst = datetime.datetime.now() - datetime.timedelta(days=1)
        dnd = datetime.datetime.now()
        # ds = self.request.GET.get('datest')
        # ds = args.get('datest', None)
   
        
        
        
        
        if self.kwargs.get('datest') != None:
            dst = self.kwargs.get('datest')
            dnd = self.kwargs.get('datend')
            dst = datetime.datetime.strptime(dst, '%d.%m.%Y')
            dnd = datetime.datetime.strptime(dnd, '%d.%m.%Y')
        # dst = self.kwargs['datest']
        # dnd = self.kwargs['datend']
        
      
        return DBTelemetry.objects.filter(datastamp__range=[dst, dnd])

# запуск mqtt
mqtt.client.loop_start()
