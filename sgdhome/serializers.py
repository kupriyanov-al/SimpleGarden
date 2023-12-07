from .models import DBTelemetry
from rest_framework import serializers


class DBTelemetrySerializer(serializers.ModelSerializer):
    
    datastamp = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    temperatura = serializers.DecimalField(max_digits=4, decimal_places=2)
    humidity = serializers.DecimalField(max_digits=4, decimal_places=1)
    coolState = serializers.BooleanField()
    releState = serializers.BooleanField()
    class Meta:
        model = DBTelemetry
        fields = ('datastamp', 'temperatura',
                  'humidity', 'coolState', 'releState')
