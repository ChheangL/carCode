from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from PIL import Image
from time import sleep
import matplotlib

matplotlib.rcParams['backend']='cairo'
matplotlib.get_backend()

frame1 = Frame(640,480,15)
cam = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc('M','J','P','G')
cam.set(6,codec)
cam.set(5,30)
cam.set(3,1028)
# it works setting the resolution
cam.set(4,720)
# but the picture color.

def main():
    while True:
        try:
#             img = Image.open('image/img21.jpg')
            ret, img = cam.read()
            if ret is False:
                raise IOError
            print('resolution: ',np.array(img).shape)
            imshow(np.array(img))
            cv2.waitKey(1)
            points,mid_points,myAngle = retrieve_angle(s1=50,h1=3, hd=10,layer = 2,img_path=img, frame=frame1)
            print(np.mean(myAngle))
            for key in frame1.fline.keys():
                plt.plot(frame1.fline[key][:,0],frame1.fline[key][:,1],'w.')
            try:
                plt.plot(points[:,0],points[:,1],'bo')
            except:
                continue
            plt.axis([0,640,480,0])
            plt.show()

    
        except KeyboardInterrupt:
            break  
    cam.release()
    cv2.destroyAllWindows()

        
main()