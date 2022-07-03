import numpy as np
import matplotlib.pyplot as plt

class EdgeFinder :
    """
       This is an improve version of 3sigma method
    """
    def __init__(self,s1,move,hd,Data):
        self.data = Data
        self.s1 = s1
        self.hd = hd
        self.move = move
        self.perform_3sig()
        
    

    def perform_3sig(self):
        BND = np.zeros([1])
        a = 0
        b = self.s1
        while True:
            segCal = self.data[a:b,:]
            plusCheck = np.mean(segCal,axis=0) + 3* np.std(segCal,axis=0)
            minusCheck = np.mean(segCal,axis=0) - 3* np.std(segCal,axis=0)
            if(b+hd) > len(self.data): hd = len(self.data)-b
            test = self.data[b-1:b+hd,:]
            checktop = (test > plusCheck)+(test<minusCheck)
            index = np.min(checktop,axis=0)
            tempBND = np.where(index==0,index,index+(b-2))
            BND = np.where(BND==0,tempBND,BND)
            x = [plusCheck,minusCheck,checktop,test,a]
            #if a == 15:
                #print(BND,x)
            a= a+self.h1
            b= b+self.h1
            if b >len(self.data): break
        return BND
     
    