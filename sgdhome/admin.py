from django.contrib import admin
from .models import DBTelemetry



# Register your models here.

@admin.register(DBTelemetry)
class DBTelemetryAdmin(admin.ModelAdmin):
    list_display = ('datastamp', 'temperatura',
                    'humidity', 'coolState', 'releState')
    # поиск
    search_fields = ('datastamp',)
