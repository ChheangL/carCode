import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self,s1,move,hd,Data,sense = 2):
        self.data = Data
        self.s1 = s1
        self.hd = hd
        self.move = move
        self.sense = sense
        self.perform_3sig()
        
    #get the upper and lower bound
    def get_3sigmaBound(self,data):
        mean = np.mean(data)
        standard_div = np.std(data)
        return [mean, standard_div*3]
    
    #the function that do the stuff above
    def check_abnormal(self,init):
        states=0 #empty dictionary discribing the current interveral data
        end=init+self.s1 #a stop for the s1 interval
        states = end #start checking at that posision of data
        x=0
        #get the upperbound and lowerbound of the data
        mean,Three_standard_div = self.get_3sigmaBound(self.data[init : end])
        #loop and check for abnormal data with upper and lower bound
        for Data in self.data[end:end+self.hd]:
            #if found abnormal, return the dictionary
            Data = np.abs([Data-mean])
            self.num = np.append(self.num,[[Data[0],Three_standard_div]],axis=0)
            print(self.num)
            if Data >= Three_standard_div: 
                if x >= self.sense:
                    return states
                else:
                    x = x+1
            elif x > 0:
                x = 0
            states += 1
        #loop is done, and num is noted at Nan
        states = np.NaN
        return states

    def perform_3sig(self):
        init = 0 #act as the starting position for the operation
        #result = {'up':[],'low':[]} #empty dictionary for result appending
        result = {}
        x=0
        self.num = np.empty((0,2),float)
        while True:
            #limter for operation going over the data value
            if init+self.s1+self.hd >= len(self.data) : 
                result['num'] = np.NaN
                break
            #call in the operation to check the abnormal value
            states = self.check_abnormal(init)
            #result['low'].append(states['low']) # append everything to the result
            #result['up'].append(states['up'])
            #check if the data found a abnormal. if so, the operation terminate
            #if np.isnan(states) and x>0:
            #    x = 0
            #elif not np.isnan(states) : 
            #    x = x+1
            if not np.isnan(states) : #and x == self.sense:
                result['num'] = states
                break
            #move to next hd
            init += self.move 
        self.abnormal = result
        return result
     
    