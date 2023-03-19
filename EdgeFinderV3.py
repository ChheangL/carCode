import numpy as np
import matplotlib.pyplot as plt
from ImageFrame import Frame

class BoundaryDetector:
    def __init__(self,data,kernal,frame,steps,T_hold) -> None:
        self.data = data
        self.kernal = kernal
        self.steps = steps
        self.threshold = T_hold
        self.frame1 = frame
        self.boundary = self.find_boundary()

    def find_boundary(self):
        offset = (self.data.size-9)%(self.kernal.size+self.steps)
        points = np.empty([0,2])
        for i in range(0,self.data.shape[1]):
                detection = False
                for t in range(20,self.data.shape[0]-offset,self.kernal.size+self.steps):
                    datas_segment = self.data[t:t+self.kernal.size,i]
                    dot_result = self.kernal.dot(datas_segment)
                    #print(dot_result)
                    if np.abs(dot_result) > self.threshold:
                        #print(t)
                        points=np.append(points,[self.frame1.fline[str(i+1)][t]],axis=0)
                        #boundary_index += [t]
                        detection = True
                        break
                if not detection:
                    points=np.append(points,[[0,0]],axis=0)
                    #boundary_index += [0]
                    detection = False
        return points
    
    def ploting_onImage(self,img,id=0):
        plt.imshow(img)
        for key in self.frame1.fline.keys():
            plt.plot(self.frame1.fline[key][:,0],self.frame1.fline[key][:,1],'k.')
        plt.title("Image {num}".format(num=id))
        plt.plot(self.boundary[:,0],self.boundary[:,1],"ro")
        plt.show()
        
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