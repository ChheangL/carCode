from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import numpy as np
from picamera import PiCamera
import matplotlib.pyplot as plt
from hardwareControl import *
import time
"""
The main function use frame and retrieve_angle function to get the boundary from the images
"""
#Setting up the Camera instances and it resolution

camera = PiCamera() #start the pi camera as camera
camera.rotation = 180
camera.resolution = (1280,720)
camera.framerate=30
camera.start_preview(alpha=200)


#Setting up the frame instances and it size
frame1 = Frame(1280,720,10)
#This is an empty array to store the 
img = np.empty((720,1280,3),dtype=np.uint8)


#Setting up a Global Variable
previous_angle = 0


def main():
#    fileNumber = 0
    while True:
        start_time = time.time()
        camera.capture(img,format='rgb')
        myAngle,_,points = retrieve_angle(s1=50,h1=4, hd=5,layer=0,img_data=img, frame=frame1)
        print("--- %s seconds ---" %(time.time()-start_time))

        if np.isnan(np.mean(myAngle[0])):
            print("Data is not found!!!!")
            continue
        myAngle1 = np.mean(myAngle[0])
        myAngle2 = np.mean(myAngle[1])

        print(myAngle)
#         print(timeit.default_timer() - start1,' ',myAngle)
        send(int(myAngle1),int(myAngle2))
#        process_figure(img,points,allPoints,myAngle,fileNumber)
#       fileNumber += 1
            

#Debugging testing the image and algorthm, It save to the 
def process_figure(img,points,allPoints,myAngle,fileNumber):
    plt.imshow(img)
#     plt.savefig("raw/image"+str(fileNumber)+".png",bbox_inches='tight')
    plt.plot(points[:,0],720-points[:,1],"ro")
    plt.plot(allPoints[:,0],allPoints[:,1],'b.')
    plt.plot([1280/2,(1280/2)+100*np.cos(np.deg2rad(((-1)*myAngle)+90))],[720,720-100*np.sin(np.deg2rad(((-1)*myAngle)+90))])
    plt.savefig("plot/image"+str(fileNumber)+".png",bbox_inches='tight')
    plt.close()
    

    
#The program start here
main()
