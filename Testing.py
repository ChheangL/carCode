from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
from gpiozero import Servo,Motor
from time import sleep
import cv2
import numpy as np

frame1 = Frame(640,480,10)

cam = cv2.VideoCapture(0)

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
        angleValue = (2/180 * angle - 1)
        servo.value = angleValue
        print("Angle: ", angleValue)
        sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")


def main():
	print('move forward')
	motor.forward(1)
	while True:
		img = np.array(cam.read()[1])
		#print(img.shape)
		myAngle = retrieve_angle(s1=60, hd=10, img_path=img, frame=frame1)
		print(myAngle.shape)
		if myAngle.shape >= (4,):
			myAngle = int(myAngle[1])
		else :
			myAngle = 90
		if myAngle <= 80 or myAngle >= 100 : 
			print('slow')
			motor.forward(0.5)
		else:
			print('fast')
			motor.forward(1)
		servo_begin(servo=myServo, angle=myAngle)


main()
