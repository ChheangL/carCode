from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
#from debug_mode import debugging
from gpiozero import Servo, Motor,Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import cv2
import numpy as np
import math
import timeit

frame1 = Frame(640,480,10)
cam = cv2.VideoCapture(0)
Device.pin_facotry = PiGPIOFactory()
#init servo
gpioPin = 4
correction = 0.45
maxPW = (2.0 + correction) / 1000
minPW = (1.0 - correction) / 1000
myServo = Servo(gpioPin, min_pulse_width=minPW, max_pulse_width=maxPW)

#init motor
print('init motor')
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)

def servo_begin(servo, angle):
	try:
		print("Angle: ", angle)
		angleValue = (2/180 * angle - 1)
		servo.value = angleValue
		#sleep(1)
	except KeyboardInterrupt:
		print("Program stopped")


def main():
    while True:
        start = timeit.default_timer()
        img = cam.read()[1]   
        try:
            print(len(img))
        except:
            print("Cam Not Found Bra")
            break
        myAngle = retrieve_angle(s1=70,h1=3, hd=10,layer = 2,img_path=img, frame=frame1)[2]
        #debugging(img, myAngle, points, mid_points)
        if not np.isnan(myAngle[0]):
            myAngle = myAngle[1]
        else:
            continue
        if myAngle <= 80 or myAngle >= 100 :
            print('slow: ',myAngle)
            motor.forward(0.15)
        else:
            print('fast: ',myAngle)
            motor.forward(0.25)
        
        servo_begin(servo=myServo, angle=myAngle)

def debug():
     while True:
        start = timeit.default_timer()
        img = cam.read()[1]
        #cv2.imwrite('~/Desktop/testimage/img'+str(x)+'.jpg', img)
        #print(img.shape)
        myAngle = retrieve_angle(s1=60, hd=5, img_path=img, frame=frame1)
        print('runtime : '+str(timeit.default_timer() - start))

main()
