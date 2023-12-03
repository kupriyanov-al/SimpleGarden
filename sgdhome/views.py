from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

class HomePageViews(TemplateView):
    template_name = 'index.html'
    