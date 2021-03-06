from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
#from debug_mode import debugging
from gpiozero import Servo, Motor,Device
from gpiozero.pins.pigpio import PiGPIOFactory
import cv2
import numpy as np
from hardwareControl import *
#import math
#import timeit

frame1 = Frame(640,480,15)
cam = cv2.VideoCapture(0)
#Device.pin_facotry = PiGPIOFactory()
#print('pinnnnnnn: ',Device.pin_facotry )
#init servo
gpioPin = 4
correction = 0.45
maxpw = (2.0 + correction) / 1000
minpw = (1.0 - correction) / 1000
#maxpw = pulse_width(duty_cycle=99)
#minpw = pulse_width(duty_cycle=1)
#myServo = Servo(gpioPin, min_pulse_width=minpw, max_pulse_width=maxpw)

#init motor
print('init motor')
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)




def debug():
     while True:
        #start = timeit.default_timer()
        img = cam.read()[1]
        #cv2.imwrite('~/Desktop/testimage/img'+str(x)+'.jpg', img)
        #print(img.shape)
        myAngle = retrieve_angle(s1=60, hd=5, img_path=img, frame=frame1)
        #print('runtime : '+str(timeit.default_timer() - start))

def main():
    #x = 0
    myAngle = 90
    while True:
        #start = timeit.default_timer()
        img = cam.read()[1] 
        cv2.imshow('img',img)
        previousAngle = myAngle  
        try:
            len(img)
        except:
            print("Cam Not Found Bra")
            break
        myAngle = retrieve_angle(s1=30,h1=3, hd=10,layer = 2,img_path=img, frame=frame1)[2]
        #debugging(img, myAngle, points, mid_points)
        #if x > 2 : break
        #x=x+1
        if not np.isnan(myAngle[0]):
            myAngle = np.mean(myAngle)
        else:
            myAngle = previousAngle
            print('no: ',myAngle)
            #hardwareControl(myServo,myAngle,motor, 0.15)
            continue
        if myAngle <= 80 or myAngle >= 100 :
            print('slow: ',myAngle)
            #hardwareControl(myServo,myAngle,motor, 0.15)
        else:
            print('fast: ',myAngle)
            # hardwareControl(myServo,myAngle,motor, 0.15)
        
        
        
main()
