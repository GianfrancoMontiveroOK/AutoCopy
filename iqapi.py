from sqlite3 import Timestamp
from iqoptionapi.stable_api import IQ_Option
import time 
from Analista import stream


API = IQ_Option('montiverogianfranco2709@gmail.com','gamemodes100')

API.connect()

API.change_balance('PRACTICE')

while True:
    if API.check_connect() == False:
        print("Error al conectar")
        API.connect()
    else:
        print("Conectado Con Exito")
        break
    
    time.sleep(1)



status,id = API.buy(1,"EURUSD",1)


#Operacion(1,"EURUSD","Call",1)