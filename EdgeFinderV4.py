import numpy as np
import matplotlib.pyplot as plt
from ImageFrame import Frame
from numba import njit

class BoundaryDetector:
    def __init__(self,img,kernal,frame,steps,T_hold) -> None:
        self.img = img
        self.kernal = kernal
        self.steps = steps
        self.threshold = T_hold
        self.frame1 = np.array(list(frame.fline.values()))
        self.frame = frame
        self.offset = (img[0].size-9)%(kernal.size+steps)
        self.sample_point = np.zeros([8,2])
        self.boundary = self.find_boundary(self.img,self.kernal,self.frame1,self.offset,self.steps,self.threshold,self.sample_point)


    @staticmethod
    @njit(nogil=True)
    def find_boundary(img,kernal,frame1,offset,steps,threshold,SP):
        points = np.empty_like(SP)
        for num,fline in enumerate(frame1):        
                detection = False
                for t in range(20,fline.shape[0]-offset,kernal.size+steps):
                    if np.abs(np.sum(kernal*np.array([img[y,x,0] for x,y in fline[t:t+kernal.size]]))) > threshold:
                        points[num]=fline[t]
                        detection = True
                        break
                if not detection:
                    points[num]=np.array([0,0])
                    detection = False
        return points
        
    def ploting_onImage(self,img,id=0):
        plt.imshow(img)
        for key in self.frame.fline.keys():
            plt.plot(self.frame.fline[key][:,0],self.frame.fline[key][:,1],'k.')
        plt.title("Image {num}".format(num=id))
        plt.plot(self.boundary[:,0],self.boundary[:,1],"ro")
        
    def ploting_onGraph(self):
        for i,j in enumerate(self.boundary[:,0]):
            plt.plot(range(0,self.data.shape[0]),self.data[:,i],'k.')
            if not j:
                plt.show()
                continue
            if not i%2:
                plt.plot([j-self.data.shape[0],j-self.data.shape[0]],[0,160],'r-')
                #print(f'{j}-{data.shape[0]}={j-data.shape[0]}')
            else:
                plt.plot([self.data.shape[0]-j,self.data.shape[0]-j],[0,160],'r-')
            plt.show()