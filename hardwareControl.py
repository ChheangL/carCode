from gpiozero import Servo, Motor,Device
from gpiozero.pins.pigpio import PiGPIOFactory

def servo_begin(servo, angle):
	try:
		print("ServoAngle: ", angle)
		angleValue = (2/180 * angle - 1)
		servo.value = angleValue
	except KeyboardInterrupt:
		print("Program stopped")

def pulse_width(duty_cycle, period=0.02):
    return duty_cycle*period/100

def degree(pulse_width, max_pw=0.019):
    return pulse_width*180/max_pw

def hardwareControl(servo,carAngle, mymotor,motorSpeed):
    mymotor.forward(motorSpeed)
    servo_begin(servo=servo, angle = carAngle)