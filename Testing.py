from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
from PIL import Image
import cv2

frame1 = Frame(1000,667,30)
img = Image.open('road1.jpg')
#cam = cv2.VideoCapture(0)


def main():
		x=1
    while True:
        #img = cv2.cvtColor(cam.read()[1],cv2.COLOR_BGR2GRAY)
        angle = retrieve_angle(s1= 60,hd=5,img_path = img,frame = frame1)
        print(x)
		x= x+1
    
main()
