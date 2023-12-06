from .models import DBTelemetry
from datetime import datetime


def recdb(datastamp, temperatura, humidity, coolState, releState):
  recordDB = DBTelemetry(datastamp=datetime.strptime(datastamp, '%d.%m.%Y %H:%M:%S'),
                         temperatura=temperatura,
                         humidity=humidity,
                         coolState=coolState,
                         releState=releState)
  recordDB.save()
