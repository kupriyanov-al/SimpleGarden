from .models import DBTelemetry
from datetime import datetime


def recdb(datastamp, temperatura, humidity, coolState, releState):
  recordDB = DBTelemetry(datastamp=datetime.strptime(datastamp, '%d.%m.%Y %H:%M:%S'),
                         temperatura=temperatura,
                         humidity=humidity,
                         coolState=coolState,
                         releState=releState)
  
  try:
    recordDB.save()
  except Exception as err:
    print(err)
    # raise Exception(f'Ошибка записи в БД. Info: {err}')
    
