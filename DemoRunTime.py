from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import numpy as np
from picamera import PiCamera
import matplotlib.pyplot as plt
from hardwareControl import *
import timeit
from EdgeFinderV2 import EdgeFinder as ef
"""
The main function use frame and retrieve_angle function to get the boundary from the images
"""
#Setting up the Camera instances and it resolution

camera = PiCamera() #start the pi camera as camera
camera.rotation = 180
camera.resolution = (1280,720)
camera.framerate=30
#camera.start_preview(alpha=200)


#Setting up the frame instances and it size
frame1 = Frame(1280,720,10)
#This is an empty array to store the 
img = np.empty((720,1280,3),dtype=np.uint8)


#Setting up a Global Variable
previous_angle = 0


def main():
    fileNumber = 0
    t1 = timeit.default_timer()
    #camera.capture("TestingImage/Image"+str(fileNumber)+".jpg")
    camera.capture(img,format='rgb')
    t2 = timeit.default_timer()
    data = frame1.get_data(img,0) #select the data
    t3 = timeit.default_timer()
    edges = ef(50,4, 5,data)
    t4 = timeit.default_timer()
    print("Capture time = ",t2-t1)
    print("CaptureFrame time = ",t3-t2)
    print("Detection time = ",t4-t3)
    print(edges.BND)
    
#The program start here
main()

