from django.shortcuts import render
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
    queryset = DBTelemetry.objects.all()
    serializer_class = serializers.DBTelemetrySerializer
  

# запуск mqtt
mqtt.client.loop_start()
