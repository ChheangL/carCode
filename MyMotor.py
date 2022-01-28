import RPi.GPIO as GPIO

class Mymotor :
    
    def __init__(self,in1,in2,en):
        GPIO.cleanup()
        self.in1 = in1;GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        self.in2 = in2
        GPIO.setup(self.in2,GPIO.OUT)
        self.en = en
        GPIO.setup(self.en,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.p=GPIO.PWM(self.en,1000)
        print('init-motor complete')


    
    def move_forward(self,speed):
        self.p.start(speed)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        print('moving forward')
        
    def move_backward(self,speed):
        self.p.start(speed)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        print('moving backward')
        
    def stop(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        print('stopped')
