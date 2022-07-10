import numpy as np
import matplotlib.pyplot as plt
from picamera import PiCamera
from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
from EdgeFinderV2 import EdgeFinder as ef
from ImageFrame import Frame
from time import sleep
camera = PiCamera()

camera.resolution = (1280,720)
camera.framerate=30
camera.rotation = 180
#frame1 = Frame(1280,720,10)

# camera.start_preview()
array = np.empty((720,1280,3),dtype=np.uint8)
for i in range(1,100,1):
	camera.capture("TestingImage/Image"+str(i)+".jpg")
	print("sleeping")
	sleep(5)
	print("wakeup")
# 
# data = frame1.get_data(array,0) #select the data    
# edges = ef(50,5, 6,data) #calculate the Boundary
# print(edges.BND)

    #Covert eges.BND to the x-y coordinates
# allPoints = np.array([frame1.fline[i][int(edges.BND[int(i)-1])]for i in frame1.fline.keys()])
# print(allPoints)


# plt.gray()
# plt.imshow(array)
# plt.plot(allPoints[:,0],allPoints[:,1],'b.')
# plt.show()
