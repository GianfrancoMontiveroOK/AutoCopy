

#texto1 = "[USDJPY-OTC Comprar 🔼 1 minuto] Riesgo: 🟢 (bajo) Zona de reacción: [98.83457 ~ 98.8245] Hora: XX:38:55"

def reaccion(texto):

    referencia=0
    posicion=0
    global valor1
    global valor2
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
    if "Vender" in texto:
        direccion="Put"
    return direccion

def par (texto):
    global par
    par =" "
    if "EURUSD" in texto:
        par="EURUSD"
    if "EURUSD-OTC" in texto:
        par="EURUSD-OTC"
    if "EURJPY" in texto:
        par="EURJPY"
    if "EURJPY-OTC" in texto:
        par="EURJPY-OTC"
    if "EURGBP-OTC" in texto:
        par="EURGBP-OTC"
    if "EURGBP" in texto:
        par="EURGBP"
    if "EURCHF" in texto:
        par="EURCHF"
    if "EURNZD" in texto:
        par="EURNZD"
    if "USDJPY" in texto:
        par="USDJPY"
    if "USDJPY-OTC" in texto:
        par="USDJPY-OTC"
    if "AUDUSD" in texto:
        par="AUDUSD"
    if "NZDUSD-OTC" in texto:
        par="NZDUSD-OTC"
    if "GBPJPY" in texto:
        par="GBPJPY"
    if "GBPJPY-OTC" in texto:
        par="GBPJPY-OTC"
    if "AUDJPY" in texto:
        par="AUDJPY"
    if "AUDCAD" in texto:
        par="AUDCAD"
    if "AUDCAD-OTC" in texto:
        par="AUDCAD-OTC"
    
def temporalidad(texto):
    global temporalidad
    temporalidad=0
    if "1 minuto" in texto:
        temporalidad=1
    if "2 minuto" in texto:
        temporalidad=2
    if "5 minuto" in texto:
        temporalidad=5
   



####################### ANALISIS DE DATOS ###########################
""""
reaccion(texto1)
par(texto1)
temporalidad(texto1)

print ("Proceso de analisis de...  " + par)
print ("Se realizo una operacion: "+ entrada(texto1))
print ("Con un Vencimiento a "+ str(temporalidad) + " Minuto/s")
print ("Momento de compra entre: "+ valor1+" y " +valor2)
"""
############## LECTURA COMPLETA #######################
"""
par = NOMBRE DEL PAR
entrada = COMPRAR/VENDER
temporalidad = VENCIMIENTO 1/2/5 MINUTOS
valor1 = PRECIO MAXIMO DE ENTRADA
valor2 = PRECIO MINIMO DE ENTRADA
"""


