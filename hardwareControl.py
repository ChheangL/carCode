from gpiozero import Servo, Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory

def ServoControl(servo, angle):
    try:
        angle=angle+90
        if angle < 45:
            angle = 45
        elif angle > 135:
            angle = 135
            
        angleValue = (2/180 * angle - 1)
        servo.value = angleValue
#         print("ServoAngle: ", angleValue)
            
    except KeyboardInterrupt:
        servo.detach()
#         print("Program stopped")

def pulse_width(duty_cycle, period=0.02):
    result = round(duty_cycle * period / 100, 4)
#     print('pulse_width: ', result)
    return result

def degree(pulse_width, max_pulse_width=0.002, degree_of_motor=180):
    result = round(pulse_width * degree_of_motor / max_pulse_width, 4)
#     print('pulse_width:', pulse_width, '= degree:', result)
    return result

def MotorControl(myMotor, speed):
    myMotor.forward(speed)