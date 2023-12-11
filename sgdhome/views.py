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

    def get_queryset(self, *args):
        # выводим из БД данные за сутки
        startDate = datetime.datetime.now() - datetime.timedelta(days=1)
        endDate = datetime.datetime.now()
        # ds = self.request.GET.get('pk')
        ds =  args.get('pk', None)
        return DBTelemetry.objects.filter(datastamp__range=[startDate, endDate])

# запуск mqtt
mqtt.client.loop_start()
