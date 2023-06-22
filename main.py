import time
from Emailing import send_email
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
time.sleep(1)
first_frame = None
while True:

    check, frame =cap.read()
    gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    gray_frame_gua = cv.GaussianBlur(gray_frame,(21,21),0)

    if first_frame  is None:
        first_frame =gray_frame_gua

    delta_frame = cv.absdiff(first_frame,gray_frame_gua)

    threshold_frame = cv.threshold(delta_frame,60,2555,cv.THRESH_BINARY)[1]
    dif_frame = cv.dilate(threshold_frame, None, iterations =2)

    #cv.imshow("My video", dif_frame)

    contours, check = cv.findContours(dif_frame,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    for conter in contours:
        if cv.contourArea(conter)<10000:
            continue
        x, y, w, h = cv.boundingRect(conter)
        rectangle = cv.rectangle(frame,(x,y),(x+w, y+h),(0, 255,0),3)
        if rectangle.any():
            send_email()
    cv.imshow("video ", frame)


    key = cv.waitKey(1)

    if key == ord("q"):
        break

cap.rielease()
