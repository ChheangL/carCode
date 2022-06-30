from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import numpy as np
from hardwareControl import *
import timeit
from picamera import PiCamera
from gpiozero import LED #import RPi.GPIO as GPIO
import matplotlib.pyplot as plt


RedLED = LED(5)
GreenLED = LED(4)


"""
Light indicate the operation of the code:
Green Light turn on when picture is taking and turn off when calculation is done
Red light indicate the angle is empty or error

Pi Camera is uses to capture image in this version of code
    The image capture in RGP formate and store in Numpy Array (1280*720*3) to use

"""

camera = PiCamera() #start the pi camera as camera
camera.rotation = 180
camera.resolution = (1280,720)
camera.framerate=30

frame1 = Frame(1280,720,10)
img = np.empty((720,1280,3),dtype=np.uint8)

# Ruduce Jitter
Device.pin_factory = PiGPIOFactory()

# min: 0.0002  mid: 0.01  max: 0.0197
min_pulse = pulse_width(duty_cycle=2)  # 0.5ms
max_pulse = pulse_width(duty_cycle=12) # 2.5ms

# min_pulse_width=1ms,  max_pulse_width=2ms,  frame_width=20ms
servo = Servo(pin=4, min_pulse_width=min_pulse, max_pulse_width=max_pulse)
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)
# servo pin is 4 5v and gnd
# motor pin are 23 24 25 and gnd

previous_angle = 0


def main():
    while True:
       try:
        GreenLED.on() # Green LED action
        camera.capture(img,format='rgb')
        myAngle,allPoints,points = retrieve_angle(s1=50,h1=4, hd=5,layer = 0,img_path=img, frame=frame1)
        myAngle = np.mean(myAngle)
        plt.imshow(img)
        plt.plot(points[:,0],720-points[:,1],"ro")
        plt.plot(allPoints[:,0],allPoints[:,1],'b.')
        plt.plot([1280/2,(1280/2)+100*np.cos(np.deg2rad(((-1)*myAngle)+90))],[720,720-100*np.sin(np.deg2rad(((-1)*myAngle)+90))])
        GreenLED.off()
        RedLED.off()
        print(myAngle)
#         print(timeit.default_timer() - start1,' ',myAngle)
        ServoControl(servo, myAngle)
        plt.show()

        if myAngle >-20.0 and myAngle < 20.0:
            MotorControl(motor, speed=0.2)
        else:
            MotorControl(motor, speed=0.15)
       except:
            servo.detach()
            motor.stop()
            break 
#     cam.release()


main()
