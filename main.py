from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import cv2
import numpy as np
from hardwareControl import *
import timeit

frame1 = Frame(1280,720,10)
cam = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc('D','I','V','X')
cam.set(6,codec)
cam.set(5,1)
cam.set(3,1280)
# it works setting the resolution
cam.set(4,720)
# but the picture color.

# Ruduce Jitter
Device.pin_factory = PiGPIOFactory()

# min: 0.0002  mid: 0.01  max: 0.0197
min_pulse = pulse_width(duty_cycle=2.5)  # 0.5ms
max_pulse = pulse_width(duty_cycle=12.5) # 2.5ms

# min_pulse_width=1ms,  max_pulse_width=2ms,  frame_width=20ms
servo = Servo(pin=4, min_pulse_width=min_pulse, max_pulse_width=max_pulse)

motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)


def main():
    while True:
        try:
#             start = timeit.default_timer()
            ret, img = cam.read()
            if ret is False:
                raise IOError
            cv2.imshow('frame',img)
            cv2.waitKey(1)

#             print('resolution: ',np.array(img).shape)
            allPoints,points,mid_points,myAngle = retrieve_angle(s1=50,h1=3, hd=10,layer = 0,img_path=img, frame=frame1)
            try:
#                 print(myAngle)
                
                myAngle = np.mean(myAngle)
#                 print(myAngle)
            except:
                continue
            
            ServoControl(servo, myAngle)
            MotorControl(motor, speed=0.15)
#             print('runtime : '+str(timeit.default_timer() - start))
        except :
            servo.detach()
            motor.stop()
            break  
    cam.release()


main()
