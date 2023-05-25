import numpy as np
import matplotlib.pyplot as plt
from ImageFrame import Frame
from numba import njit

class BoundaryDetector:
    def __init__(self,img,kernal,frame,T_hold) -> None:
        self.img = img
        self.kernal = kernal
        self.threshold = T_hold
        self.frame1 = np.array(list(frame.fline.values()))
        self.frame = frame
        self.sample_point = np.zeros([len(frame.fline),2])
        self.boundary, self.conv_resutl= self.find_boundary(self.img,self.kernal,self.frame1,self.threshold,self.sample_point)
#Jit complie here
    @staticmethod
    @njit(nogil=True)
    def find_boundary(img,kernal,frame1,threshold,SP):
        points = np.empty_like(SP)
        conv_result = np.zeros_like(frame1[:,:,0])
        
        for num,fline in enumerate(frame1):        
                detection = False
                i =0 
                for t in range(20,fline.shape[0]):      #looping through all the lines
                    #if value or size over the image : skip to next line
                    if t+kernal.size > len(fline) or fline[t+kernal.size][0]==0: continue  
                    #Populate data and convolution in a single line
                    conv_result[num][i] = np.abs(np.sum(kernal*np.array([img[int(y),int(x),0] for x,y in fline[t:t+kernal.size]])))
                    #Check the result with threshold
                    if conv_result[num][i] > threshold:
                        points[num]=fline[t]
                        if points[num][1] > 365: # A cheap trick to skip the first 5 pixels
                            detection = True #flag for condition below
                        break
                    i = i + 1 #counter for iterating conv_result
                if not detection:
                    points[num]=np.array([0,0])
                    detection = False
        return points,conv_result
#Jit end pre-compile here
       
    def ploting_onImage(self,img,id=0):
        #plot image
        plt.imshow(img)
        #plot the masks and lines
        for key in self.frame.fline.keys():
            plt.plot(self.frame.fline[key][:,0],self.frame.fline[key][:,1],'k,')
        plt.title("Image {num}".format(num=id))
        #show the boundary on the image
        plt.plot(self.boundary[:,0],self.boundary[:,1],"ro")
        
    def ploting_onGraph(self):
        data = np.empty([int(self.frame.width/2.0),0],int)
        for key in self.frame.fline.keys():
            data = np.append(data,np.array([[self.img[int(y),int(x),0]] for x,y in self.frame.fline[key]]),axis=1)
        
        for i,j in enumerate(self.boundary[:,0]):
            #plot the data
            plt.plot(range(0,data.shape[0]),data[:,i],'k.')
            #plot the convolution results
            plt.plot(range(int((len(self.kernal))/2)+20,self.conv_resutl.shape[1]+int((len(self.kernal))/2)+20),self.conv_resutl[i,:],'b-')
            if not j:
                plt.show()
                continue
            #plot the boundary detected
            if not i%2:
                plt.plot([j-data.shape[0],j-data.shape[0]],[100,160],'r-')
            else:
                plt.plot([data.shape[0]-j,data.shape[0]-j],[100,160],'r-')
            plt.show()