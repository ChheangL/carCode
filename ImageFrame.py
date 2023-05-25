import numpy as np
import pickle as pk
import math 

class Frame:
    """get the coordinate to the lines based on the angle, width and hight provided
    """
    def __init__(self, width, height, angle):
            self.width = width
            self.height = height
            self.angle = angle
            try:
                #if there is a file for that frame, then we don't need to calculate the frame again
                self.fline = self.deSerialize().fline
            except:
                #if file is not found (That what the exception are for), then we calculate using get_frame_coordinate method for the angle
                print('Calculating Frame ...')
                self.fline = {}
                i = 1
                while angle*i < 50: #maximum value of angle 
                    tempRight,tempLeft = self.get_frame_coordinate(width=self.width,h=self.height,theta=angle*i)
                    self.fline[str(2*i-1)] = tempRight #saving the temp right to 1,3,5,7 ...
                    self.fline[str(2*i)] = tempLeft    #saving the temp left to  2,4,6,8 ...
                    i = i+1
                self.serialize()
                print('Done!')
        
    def get_frame_coordinate(self,width,h,theta):
        height = int(h/2) #using the height/2 to mask the top half of the image
        print('angle = '+str(theta)+', width='+str(width)+', height'+str(height))
        tan = math.tan(math.radians(theta))         #calcuate the tan value of that angle
        lr = np.zeros([int(width/2),2]) 
        lr[0]=[int(width/2)-1,h-1]  #init the first point of the right line ex (640/2) and (720-1)
        ll = np.zeros([int(width/2),2]) 
        ll[0] =[int(width/2)-1,h-1]   #init the first point of the left line ex same as above

        for iter in range(1,int(width/2)):      #looping the horizontal axis starting from 1
            for jter in range(1,height):        #looping the vertical axis starting from 1
                test = np.abs([tan-jter/iter])  #calculte the error between tangen and the actual value
                if test[0]<0.01:                #if the error is small push that values of right line and left line
                    lr[iter] = [int(width/2+iter-1),int(h/2+height-jter+1-1)]
                    ll[iter] = [int(width/2-iter-1),int(h/2+height-jter+1-1)]
                    break
                elif jter==height-1:                           #else the last value will be used
                    if lr[iter-1][1] > h/2+2:                   
                        lr[iter] = [int(width/2+iter-1),lr[iter-1][1]]
                        ll[iter] = [int(width/2-iter-1),ll[iter-1][1]]
                    break
                    
        return lr,ll

    
            
   # this function is use the get data from the image and return data masked by the frame 
   # for function with numba jit, this function is depricated.
    def get_data(self,img,layer=np.NaN):
        img = np.array(img)
        if not np.isnan(layer) : img = img[:,:,layer]
        #img = 255.0*(img/255.0)**6 #for blurring the image
        data = np.empty([int(self.width/2.0),0],int)
        for key in self.fline.keys():
            data = np.append(data,np.array([[img[y,x]] for x,y in self.fline[key]]),axis=1)
        return data


    #save lines_frame to Pkl as 'frame.pkl'
    def serialize(self):
        with open(('Frame/'+str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'wb') as f:
            pk.dump(self, f)
            
    def deSerialize(self):
        with open(('Frame/'+str(self.width)+'x'+str(self.height)+'_'+str(self.angle)+'frame.pkl'), 'rb') as f:
            print('load CVS file successfully')
            return pk.load(f)
        
        