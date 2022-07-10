from gpiozero import Motor
from time import sleep
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)

motor.stop()

#x =1
#while True:
#	print('.')
#	motor1.move_forward(50)
#	x = x+1
	#motor1.stop()
#	if x == 10000 : break
