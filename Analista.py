import cv2
import numpy as np

capture = cv2.VideoCapture(0)

while True:
    ret, image = capture.read

    cv2.imshow('video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break







