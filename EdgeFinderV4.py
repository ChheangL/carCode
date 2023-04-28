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
        self.sample_point = np.zeros([len(frame.fline),2])
        self.boundary, self.conv_resutl= self.find_boundary(self.img,self.kernal,self.frame1,self.steps,self.threshold,self.sample_point)


    @staticmethod
    @njit(nogil=True)
    def find_boundary(img,kernal,frame1,steps,threshold,SP):
        points = np.empty_like(SP)
        conv_result = np.zeros_like(frame1[:,:,0])
        
        for num,fline in enumerate(frame1):        
                detection = False
                i =0 
                for t in range(20,fline.shape[0]):
                    if t+kernal.size > len(fline): continue
                    conv_result[num][i] = np.abs(np.sum(kernal*np.array([img[int(y),int(x),0] for x,y in fline[t:t+kernal.size]])))
                    if conv_result[num][i] > threshold:
                        points[num]=fline[t]
                        if points[num][1] > 365:
                            detection = True
                        break
                    i = i + 1
                if not detection:
                    points[num]=np.array([0,0])
                    detection = False
        return points,conv_result
        
    def ploting_onImage(self,img,id=0):
        plt.imshow(img)
        for key in self.frame.fline.keys():
            plt.plot(self.frame.fline[key][:,0],self.frame.fline[key][:,1],'k,')
        plt.title("Image {num}".format(num=id))
        plt.plot(self.boundary[:,0],self.boundary[:,1],"ro")
        
    def ploting_onGraph(self):
        data = np.empty([int(self.frame.width/2.0),0],int)
        for key in self.frame.fline.keys():
            data = np.append(data,np.array([[self.img[int(y),int(x),0]] for x,y in self.frame.fline[key]]),axis=1)
        for i,j in enumerate(self.boundary[:,0]):
            plt.plot(range(0,data.shape[0]),data[:,i],'k.')
            plt.plot(range(int((len(self.kernal))/2)+20,self.conv_resutl.shape[1]+int((len(self.kernal))/2)+20),self.conv_resutl[i,:],'b-')
            if not j:
                plt.show()
                continue
            if not i%2:
                plt.plot([j-data.shape[0],j-data.shape[0]],[100,160],'r-')
                #print(f'{j}-{data.shape[0]}={j-data.shape[0]}')
            else:
                plt.plot([data.shape[0]-j,data.shape[0]-j],[100,160],'r-')
            plt.show()