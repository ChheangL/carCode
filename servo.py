from hardwareControl import *
from gpiozero import Servo, Motor,Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_facotry = PiGPIOFactory()
#print('pinnnnnnn: ',Device.pin_facotry )
#init servo
gpioPin = 4
correction = 0.45
maxpw = (2.0 + correction) / 1000
minpw = (1.0 - correction) / 1000
#maxpw = pulse_width(duty_cycle=99)
#minpw = pulse_width(duty_cycle=1)
myServo = Servo(gpioPin, min_pulse_width=minpw, max_pulse_width=maxpw)

#init motor
print('init motor')
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)

hardwareControl(myServo,100,motor,0)