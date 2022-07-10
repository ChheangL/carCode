import numpy as np

class EdgeFinder :
    """
       This perform the 3-sigma method on a single dimension data set
       Attribue : 
           data (numpy array)
           s1 (int)
           hd (int)
           abnormal (dictionary)
       Method :
           return(void)       __init__(self,s1,hd,data) : is a constructor
           return(list)       get_3sigmaBound(self,data_seg) : for getting the boundary in the interval
           return(dictionary) check_abnormal(self,init) : perform checking for the hd interval
           return(dictionary) perform_3sig(self) : perform the 3 sigma method for the entier data set
           return(void)       plot_data(self) : ploting the data on the graph
    """
    def __init__(self,s1,h1,hd,Data):
        self.data = Data
        self.s1 = s1
        self.hd = hd
        self.h1 = h1
        self.BND = self.perform_3sig()
        
    #get the upper and lower bound

    def perform_3sig(self):
        BND = np.zeros(self.data.shape[1])
        a = 0
        b = self.s1
        while True:
            segCal = self.data[a:b,:] #creating segment to calculate mean and Std
            plusCheck = np.mean(segCal,axis=0) + 3* np.std(segCal,axis=0)
            minusCheck = np.mean(segCal,axis=0) - 3* np.std(segCal,axis=0)
            # if hd interval is out-of-range, then just use a smaller hd
            if(b+self.hd) > len(self.data): self.hd = len(self.data)-b
            # creating hd segment for testing the 3-sigma boundaries 
            test = self.data[b-1:b+self.hd,:]
            # Check the top and bottom, return True or False Ex: [0,0,0,1,0,0 ...]
            checktop = (test > plusCheck)+(test < minusCheck)
            # 
            index = np.min(checktop,axis=0)
            tempBND = np.where(index==0,index,index+(b-2))
            BND = np.where(BND==0,tempBND,BND)
            a= a+self.h1
            b= b+self.h1
            if b >len(self.data): break
        return BND
    
    