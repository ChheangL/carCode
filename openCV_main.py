from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import numpy as np
from hardwareControl import *
import timeit
import cv2, queue, threading, time

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(3,1280)
    self.cap.set(4,720)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()






# ----------------------------------------------------------------

frame1 = Frame(1280,720,10)
cam = VideoCapture(0)


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
    x = False
    startTimer = True
    while True:
      try:
        if startTimer :
            start1 = timeit.default_timer()
        else :
            start2 = timeit.default_timer()
        img = cam.read()
        myAngle = retrieve_angle(s1=50,h1=3, hd=20,layer = 0,img_path=img, frame=frame1)
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

