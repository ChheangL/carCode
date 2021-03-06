from hardwareControl import *
import time
Device.pin_factory = PiGPIOFactory()

# min: 0.0002  mid: 0.01  max: 0.0197
min_pulse = pulse_width(duty_cycle=2)  # 0.5ms
max_pulse = pulse_width(duty_cycle=12) # 2.5ms

# min_pulse_width=1ms,  max_pulse_width=2ms,  frame_width=20ms
servo = Servo(pin=4, min_pulse_width=min_pulse, max_pulse_width=max_pulse)

ServoControl(servo, 0)

time.sleep(1)

ServoControl(servo,-90)
time.sleep(1)

ServoControl(servo,90)
time.sleep(1)

ServoControl(servo,0)
# servo.value = 1