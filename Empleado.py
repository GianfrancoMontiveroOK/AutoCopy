
from mss import mss
import cv2
import numpy as np
from PIL import Image
import pytesseract
import time
import Capturadora





mon = {'top': 0, 'left':200, 'width':800, 'height':800}
sct = mss()
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'




while True:
    ###### CAPTURA DE PANTALLA ######
    time_sleep=(1)
    sct_img = sct.grab(mon)
    ret, imgg = sct_img.read()
    img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    

    gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
    #gray = cv2.blur(gray,(3,3))
    canny = cv2.Canny(gray,400,200)
    canny = cv2.dilate(canny,None,iterations=1)

    ######### Extraccion de Fotogramas ###########
    
    ######## Zona de Lectura ############
    #cv2.rectangle(gray,(60,500),(360,700),(0,0,0),cv2.FILLED)




    ########### CONTORNOS ##############

    cnts, _ = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(gray,cnts,-1,(0,255,0),2)

    ########## DIBUJOS ##################
    #cv2.drawContours(gray,cnts,-1,(0,255,0),2  
    
    for c in cnts:
        area = cv2.contourArea(c)
        if area>26000:
            print("area= ",area)
            cv2.drawContours(gray,[c],0,(0,255,0),2)

     

    ################## EXTRAER EL ALTO Y ANCHO FOTOGRAMAS ######################
    #al,an,c = gray.shape

    #cv2.rectangle(gray,(100,300),(200,400),(0,0,0),cv2.FILLED)
    ######## DETECCION DE CARACTERES ###########
   
    
    ######## Lectura #########
    #
    #config="--psn 1"
    #texto = pytesseract.image_to_string(gray,config=config)

    ####### CONVERSION DE MATRIZ A IMAGEN ###############

    #gray = gray.reshape(al, an)
    #gray = Image.fromarray(gray)
    #gray = gray.convert("L")




    ########## SALIDA VISUAL ############
    cv2.imshow('video',gray)
    

    if cv2.waitKey(1)  & 0xFF == ord('q'):
        break
    time.sleep(1)
gray.realease()
cv2.destroyAllWindows()

    

