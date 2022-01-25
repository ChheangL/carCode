from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
from gpiozero import Servo
from time import sleep
import cv2

frame1 = Frame(1000,667,10)
cam = cv2.VideoCapture(0)

gpioPin = 4
correction = 0.45
maxPW = (2.0 + correction) / 1000
minPW = (1.0 - correction) / 1000
myServo = Servo(gpioPin, min_pulse_width=minPW, max_pulse_width=maxPW)

def servo_begin(servo, angle):
    try:
        angleValue = (2/180 * angle - 1)
        servo.value = angleValue
        print("Angle: ", angleValue)
        sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")

def main():
    while True:
        img = cam.read()[1]
        myAngle = retrieve_angle(s1=60, hd=5, img_path=img, frame=frame1)
        print(myAngle[1])
        servo_begin(servo=myServo, angle=myAngle[1])

main()
