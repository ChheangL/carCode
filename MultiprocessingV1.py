import numpy as np
import math 
from ImageFrame import Frame
from EdgeFinderV2 import EdgeFinder as ef
import concurrent.futures
import cv2 as cv
import timeit
from matplotlib import pyplot as plt

filename = "TestingImage/Image5.jpg"
img = cv.imread(filename)
img = img[:,:,0]

def framePopulate(key,frame1):
    print("Doing my best!!")
    global img
    data = [[img[y,x]] for x,y in frame1.fline[key]]
    return data


def populateData(frame1):
    global img
    data = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(framePopulate,key,frame1) for key in frame1.fline.keys()]
        for f in concurrent.futures.as_completed(results):
            data.append([f.result()])
    return data

def populateDatav2(frame1):
    global img
    data = [np.append(data,np.array([[img[y,x]] for x,y in frame1.fline[key]]),axis=1) for key in frame1.fline.keys()]
    return data

i=1
if __name__ == "__main__":
    
    print(f"loaded image{i}")
    i=+1
    frame1 = Frame(1280,720,10)
    t1 = timeit.default_timer()
    data = populateData(frame1)
    t2 = timeit.default_timer()
    dst = cv.Canny(img, 50, 200, None, 3)
    t3 = timeit.default_timer()
    print(f'populate time :{t2-t1}s')
    print(f'canny time :{t3-t2}s')


    #ploting the image
    images = [img,dst]
    title = ["Original Image", "Canny"]
    for i in range(len(images)):
        plt.subplot(2, 2, i+1) 
        plt.imshow(images[i], 'gray')
        plt.title(title[i])
        plt.xticks([]), plt.yticks([])
    plt.show()