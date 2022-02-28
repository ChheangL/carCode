from unittest import TestCase
from matplotlib.pyplot import axis
import numpy as np
import pickle as pk
import math 

class Frame:
    """get the coordinate to the lines based on the angle, width and hight provided
    """
    
        
    def get_frame_coordinate(self,width,height,theta):
        print('angle = '+str(theta)+', width='+str(width)+', height'+str(height))
        tan = math.tan(math.radians(theta))
        lr = np.array([[int(width/2)-1,height-1]])
        ll = np.array([[int(width/2)-1,height-1]])

        for iter in range(1,int(width/2)):
            for jter in range(1,height):
                test = np.abs([tan-jter/iter])
                if test[0]<0.01:
                    #print(str(iter) +' '+ str(480-jter+1))
                    lr = np.append(lr,[[int(width/2+iter-1),height-jter+1-1]],axis=0)
                    ll = np.append(ll,[[int(width/2-iter-1),height-jter+1-1]],axis=0)
                    break
                else:
                    if jter==height-1:
                        lr = np.append(lr,[[int(width/2+iter-1),lr[iter-1,1]]],axis=0)
                        ll = np.append(ll,[[int(width/2-iter-1),ll[iter-1,1]]],axis=0)
        return lr,ll

    def __init__(self, width, height, angle):
            self.width = width
            self.height = height
            self.angle = angle
            try:
                self.lines_frame = self.unserilize().lines_frame
            except:
                print('Calculating Frame ...')
                self.lines_frame = {}
                i = 1
                lineNum = int(180/angle)
                while angle*i < 90:
                    #print(i)
                    print(angle*i)
                    tempRight,tempLeft = self.get_frame_coordinate(width=self.width,height=self.height,theta=angle*i)
                    print('L'+str(lineNum-i))
                    self.lines_frame['L'+str(i)] = tempRight
                    self.lines_frame['L'+str(lineNum-i)] = tempLeft
                    i = i+1
                    
                self.serilization()
                print('Done!')
            
   
    def get_data(self,img,layer=np.NaN):
        img = np.array(img)
        if not np.isnan(layer) : img = img[:,:,layer]
        #img = 255.0*(img/255.0)**6
        #self.plot_all_line('k')
        #imshow(img)
        lines = {}
        for key in self.lines_frame.keys():
            temp2 = np.empty((0,1),float)
            for cord in self.lines_frame[key]:  
                temp1 = img[int(cord[1]),int(cord[0])]
                temp2 = np.append(temp2,[temp1])
            lines[key] = temp2
        return lines
    #save lines_frame to cvs as 'frame.cvs'

    def serilization(self):
        with open(('Frame/'+str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'wb') as f:
            pk.dump(self, f)
            
    def unserilize(self):
        with open(('Frame/'+str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'rb') as f:
            print('load CVS file successfully')
            return pk.load(f)
        
        