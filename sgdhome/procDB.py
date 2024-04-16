from .models import DBTelemetry
from datetime import datetime


class RecDB:
  
  old_temperatura, old_humidity, old_coolState, old_releState = None, None, None, None
  
  def record(datastamp, temperatura, humidity, coolState, releState):
    
    recordDB = DBTelemetry(datastamp=datetime.strptime(datastamp, '%d.%m.%Y %H:%M:%S'),
                           temperatura=temperatura,
                           humidity=humidity,
                           coolState=coolState,
                           releState=releState)
    
    # print(f"old_temperatura={RecDB.old_temperatura}")
    try:
      if (RecDB.old_temperatura != temperatura) or (RecDB.old_humidity!=humidity) or (RecDB.old_coolState!=coolState) or (RecDB.old_releState!=releState):
        recordDB.save()
        # print("Запись в БД")
      RecDB.old_temperatura, RecDB.old_humidity, RecDB.old_coolState, RecDB.old_releState = temperatura, humidity, coolState, releState
    except Exception as err:
      print(err)



# def recdb(datastamp, temperatura, humidity, coolState, releState):

#   recordDB = DBTelemetry(datastamp=datetime.strptime(datastamp, '%d.%m.%Y %H:%M:%S'),
#                          temperatura=temperatura,
#                          humidity=humidity,
#                          coolState=coolState,
#                          releState=releState)


  
#   try:
#     recordDB.save()
#     print("Запись в БД")

    
#   except Exception as err:
#     print(err)
#     # raise Exception(f'Ошибка записи в БД. Info: {err}')
    
