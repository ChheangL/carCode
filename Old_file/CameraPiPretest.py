"""
This code help abjust camera levels
"""
from picamera import PiCamera
from time import sleep


camera = PiCamera() #start the pi camera as camera
camera.rotation = 180
camera.resolution = (1280,720)
camera.framerate=30
camera.start_preview(alpha=200)
