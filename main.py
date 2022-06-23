from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import numpy as np
from hardwareControl import *
import timeit
from picamera import PiCamera

frame1 = Frame(1280,720,10)

cam = PiCamera()
cam.resolution=(1280,720)

# Ruduce Jitter
Device.pin_factory = PiGPIOFactory()

# min: 0.0002  mid: 0.01  max: 0.0197
min_pulse = pulse_width(duty_cycle=2)  # 0.5ms
max_pulse = pulse_width(duty_cycle=12) # 2.5ms

# min_pulse_width=1ms,  max_pulse_width=2ms,  frame_width=20ms
servo = Servo(pin=4, min_pulse_width=min_pulse, max_pulse_width=max_pulse)

motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)

previous_angle = 0

def main():
    while True:
      try:
        img = cam.read()
        myAngle = retrieve_angle(s1=50,h1=3, hd=20,layer = 0,img_data=img, frame=frame1)
        myAngle = np.mean(myAngle)
        print(timeit.default_timer() - start1,' ',myAngle)
        ServoControl(servo, myAngle)
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
