from ast import Not
from operator import not_
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Corredor_Bolsa import reaccion,entrada,par,temporalidad
from sqlite3 import Timestamp
from iqoptionapi.stable_api import IQ_Option

import time
from datetime import datetime
from dateutil import tz


###################### CONEXION A IQ OPTIONS ############################

API = IQ_Option('mgmail.com','PASSWORD0')

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

######################## No repeticiones ##########################
global textanterior
textanterior=""



######################## TIEMPO #############################################

def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GTM'))

    return str(hora.astimezone(tz.gettz('America/Argentina'))) [:-6]

############################## PRECIO ACTUAL A TIEMPO REAL ##############################3       ####################### ACA SE CAMBIA EL MONTO ########## VA DE A 1 ###
def stream(API,par_seleccionado,max,min,vencimiento,direccion):
    
    API.start_candles_stream(par_seleccionado,60, 1)

    vela=API.get_realtime_candles(par_seleccionado,60)
    time.sleep(1)
    analisisvelas=True
    global id
    global status
    cronometro=0
    
    
    
    while analisisvelas==True:

        for velas in vela:
            VelaTiempoReal=(vela[velas]['open'])
            
            if cronometro==0:
                status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
                compra1=VelaTiempoReal
            
            if cronometro>=40 and direccion=="Put" and compra1<=VelaTiempoReal and vencimiento==1:
                status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
                analisisvelas=False

            if cronometro>=40 and direccion=="Put" and compra1<=VelaTiempoReal and vencimiento==1:
                status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
                analisisvelas=False


            if cronometro>=70 and direccion=="Put" and compra1<=VelaTiempoReal and vencimiento==2:
                status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
                analisisvelas=False
                
            if cronometro>=70 and direccion=="Call" and compra1>=VelaTiempoReal and vencimiento==2:
               status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
               analisisvelas=False
            if cronometro>=73:
                analisisvelas=False
            print(cronometro," ",compra1," ",VelaTiempoReal," ",vencimiento," ",direccion)
            """
            if float(max) <= float(min): 
                print ("Zona de Reaccion: Precio maximo: "+ str(min) + " Precio minimo: " + str(max))
                dif = (float(min)-float(max))
                if direccion == "Call" and cronometro==0 and float(max)!=float(min):
                    min=float(min)+float(dif)
                    print ("sume diferencia")
                if direccion ==  "Put" and cronometro==0 and float(max)!=float(min):
                    max=float(max)-float(dif)
                    print ("reste diferencia")
                # alrevez
                if VelaTiempoReal <= float(min) and VelaTiempoReal >= float(max) or direccion == "Put" and VelaTiempoReal>float(min) and VelaTiempoReal>float(max) or direccion == "Call" and VelaTiempoReal<float(min) and VelaTiempoReal<float(max) or float(max)==float(min):  
                    status,id=API.buy(1000,par_seleccionado,direccion,int(vencimiento))
                    #Operacion(1000,par_seleccionado,direccion,int(vencimiento))
                    time.sleep(2)
                    analisisvelas=False

            if float(max)>=float(min):
                print ("Zona de Reaccion: Precio maximo: "+ str(max) + " Precio minimo: " + str(min))
                dif = (float(max)-float(min))
                   
                if direccion == "Call" and cronometro==0 and float(max)!=float(min) :
                    max=float(max)+float(dif)
                    print ("sume diferencia")
                if direccion ==  "Put" and cronometro==0 and float(max)!=float(min):
                    min=float(min)-float(dif)
                    print ("reste diferencia")
                    
                # derecho
                if VelaTiempoReal >=  float(min) and VelaTiempoReal <= float(max) or direccion == "Put" and VelaTiempoReal>float(min) and VelaTiempoReal>float(max) or direccion == "Call" and VelaTiempoReal<float(min) and VelaTiempoReal<float(max) or float(max)==float(min) :  
                    status,id=API.buy(1000,par_seleccionado,direccion,int(vencimiento))
                    #Operacion(1000,par_seleccionado,direccion,int(vencimiento))
                    time.sleep(2)
                    analisisvelas=False

            print ("Cronometro a 120 segundos[" + str(cronometro) + "] precio actual: " + str(VelaTiempoReal))
            """



            cronometro=cronometro+1
       


            time.sleep(1)
    API.stop_candles_stream(par_seleccionado,60)
    time.sleep(3)
       
        
    



######## SENTENCIAS #########

TOKEN="1111111111111111111111111"


#COMANDOS
def start(update, context):
    print(update.message)
    update.message.reply_text(f"Estoy Encendida")

def info(update, context):
    print(update.message)
    update.message.reply_text(f"aun no configurado")

#Funcion Encargada del analisis del Texto recibido 
def process_message(update, context):
    global text
    global id
    global status
    global textanterior
    
   
    text=update.message.text
    
    update.message.reply_text("Analizando Señal....")

    ############ valores necesarios del texto########################
    reaccion(text)
    min=valor1
    max=valor2
    direccion=entrada(text)
    par_seleccionado=par(text)
    vencimiento=temporalidad(text)

    ######## check en TERMINAL ################
    
    print ("###############################################")
    print ("Proceso de analisis de...  " + par_seleccionado)
    print ("Se realizo una operacion: "+ direccion)
    print ("Con un Vencimiento a "+ str(vencimiento) + " Minuto/s")
    print ("Momento de compra entre: "+ str(max)+" y " +str(min))
    print ("###############################################")
    ######################################################
   
    if text != textanterior:
        update.message.reply_text("Hare una operacion en "+str(par_seleccionado)+ " a "+ str(vencimiento)+ " minutos " + "con direccion :"+ direccion + ": entre los valores "+ str(min)+" y "+ str(max) )
        #status,id=API.buy(int(1000),str(par_seleccionado),str(direccion),int(vencimiento))
        #status,id=API.buy(1000,par_seleccionado,direccion,int(vencimiento))
        stream(API,par_seleccionado,max,min,vencimiento,direccion)
        update.message.reply_text("############## OPERACION REALIZADA ################")
        print ("############## OPERACION EXITOSA ################")
    else:
        update.message.reply_text("############## ERROR (SEÑAL REPETIDA) ################")
        print ("############## ERROR (SEÑAL REPETIDA) ################")

    textanterior=text
    

############################# ANALISIS DE TEXTO ##################################


def reaccion(texto):

    global valor1
    global valor2
    referencia=0
    posicion=0
    valor1=""
    valor2=""
    
   
    for i in texto:
        if referencia==3:
            valor2=valor2+i
            if i == "]":
                break
        if referencia==2:
            valor1=valor1+i
            if i == " ":
                referencia=referencia+1
        posicion=posicion+1
        if i == "[":
            referencia=referencia+1

    mapeo = {
        ord(']'):'',
        ord('~'):'',
        ord(' '):''
    }
    valor1=valor1.translate(mapeo)
    valor2=valor2.translate(mapeo)
          
def entrada(texto):
    direccion=""
    if "Comprar" in texto:
        direccion="Call"
        return direccion
    if "Vender" in texto:
        direccion="Put"
        return direccion
    if "🔼" in texto:
        direccion="Call"
        return direccion
    if "🔽" in texto:
        direccion="Put"
        return direccion

def par (texto):
    par =" "
    if "EURUSD-OTC" in texto:
        par="EURUSD-OTC"
        return par
    if "EURJPY-OTC" in texto:
        par="EURJPY-OTC"
        return par
    if "EURGBP-OTC" in texto:
        par="EURGBP-OTC"
        return par
    if "USDJPY-OTC" in texto:
        par="USDJPY-OTC"
        return par
    if "NZDUSD-OTC" in texto:
        par="NZDUSD-OTC"
        return par
    if "GBPJPY-OTC" in texto:
        par="GBPJPY-OTC"
        return par
    if "AUDCAD-OTC" in texto:
        par="AUDCAD-OTC"
        return par
    if "GBPUSD-OTC" in texto:
        par="GBPUSD-OTC"
        return par
    if "GBPJPY" in texto:
        par="GBPJPY"
        return par
    if "EURUSD" in texto:
        par="EURUSD"
        return par
    if "GBPUSD" in texto:
        par="GBPUSD"
        return par
    if "AUDJPY" in texto:
        par="AUDJPY" 
        return par
    if "AUDCAD" in texto:
        par="AUDCAD"
        return par
    if "EURJPY" in texto:
        par="EURJPY"
        return par
    if "EURGBP" in texto:
        par="EURGBP"
        return par
    if "EURCHF" in texto:
        par="EURCHF"
        return par
    if "EURNZD" in texto:
        par="EURNZD"
        return par
    if "USDJPY" in texto:
        par="USDJPY"
        return par
    if "AUDUSD" in texto:
        par="AUDUSD"
        return par
    if "NZDUSD" in texto:
        par="NZDUSD"
        return par
    if "BTCUSD" in texto:
        par="BTCUSD"
        return par
    if "XAUUSD" in texto:
        par="XAUUSD"
        return par
   
    
def temporalidad(texto):
    temporalidad=0
    if "1 minuto" in texto:
        temporalidad=1
        return temporalidad
    if "2 minuto" in texto:
        temporalidad=2
        return temporalidad
    if "5 minuto" in texto:
        temporalidad=5
        return int(temporalidad)
   
    
    
#MAIN
def main():

    while True:
        if API.check_connect() == False:
            print("Error al conectar")
            API.connect()
        else:
            print("Conectado Con Exito")
            break
    
    time.sleep(1)
    
    updater = Updater(TOKEN, use_context=True)
    
    #Comando Iniciador del main
    updater.dispatcher.add_handler(CommandHandler("start", start))

    #Comando Lector de Mensajes
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text , callback=process_message))

    #start 
    updater.start_polling()
    print("Estoy Escuchando")

    # Me quedo esperando que...
    updater.idle()
    print("estoy aca")

    if __name__ == "__main__":
        main()
main()


