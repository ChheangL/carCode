from gpiozero import Servo
from time import sleep

def servo_setup(gpioPin=4, correction=0.45):
    maxPW=(2.0 + correction) / 1000
    minPW=(1.0 - correction) / 1000
    return Servo(gpioPin, min_pulse_width=minPW, max_pulse_width=maxPW)

def servo_begin(servo, angle):
    try:
	print("Angle: ", angle)
        angleValue = (2/180 * angle - 1)
        servo.value = angleValue
        sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")
