from pickle import TRUE

import cv2 as cv
import cv2
import numpy as np
import os
import time
from PIL import Image
import pytesseract
import autogui as pa
from AccionReenvio import accionReenvio
from AccionReenvio import accionActualizar

from Capturadora import WindowCapture

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WindowCapture.list_window_names()
contador=0
global targetglobal
targetglobal="xd"
# initialize the WindowCapture class
wincap = WindowCapture('Telegram')
targetlocal=None
def reco(target):
    global targetglobal
    if targetglobal=="xd":
        #print("sin valor")
        targetglobal=target
        accion=True
        return accion
    elif targetglobal==target:
        #print("SIN CAMBIOS")
        accion=True
        targetglobal=target
        return accion
    elif target!=targetglobal:
        accion=False
        targetglobal=target
        return accion

    



while(True):
    time.sleep(3)
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    recorte = screenshot[600:700,300:800]

    #recorte = cv2.dilate(recorte,None,iterations=1)
  
    pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    target = pytesseract.image_to_string(recorte,config='--psm 1')
    print (target)
    if reco(target)==False:
        print("####### ACCION DE REENVIO ######")
        accionReenvio()
    else:
        accionActualizar()
        
    
   
    



    




    
    #cv2.imshow("vision",recorte)
    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()
    

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')