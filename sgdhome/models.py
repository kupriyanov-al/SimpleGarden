
from django.db import models


# Create your models here.
class DBTelemetry( models.Model):
    datastamp = models.DateTimeField(
        'Дата', auto_now=False, auto_now_add=False, db_index=True, unique=True)
    temperatura = models.DecimalField('Температура', null=True, max_digits=4, decimal_places=2)
    humidity = models.DecimalField(
        'Влажность', null=True , max_digits=4, decimal_places=1)
    coolState = models.BooleanField('Вентилятор')
    releState = models.BooleanField('Освещение')
    
    def __str__(self):
        return (f"datastamp={self.datastamp}. temperatura= {self.temperatura}.humidity ={self.humidity} coolState = {self.coolState} releState = {self.releState}")
 