import numpy as np
import math
from ImageFrame import Frame
from EdgeFinder import EdgeFinder as ef


def mid_angle(data,width,height):
    data_size = int(len(data))
    values = np.empty((0,3),float)
    for i in range (0, data_size,2):
        mid = (data[i] + data[i+1])/2
        if mid[0]-(width/2.) != 0.0:
            tan = (mid[1]-height)/(mid[0]-(width/2.))
            angle_radiant = math.atan(tan)
            angle_degree = math.degrees(angle_radiant)
            #print(angle_degree)
            angle = ((-1)*angle_degree if angle_degree < 0 else 180-angle_degree)
        else :
            angle = 90.0
        values = np.append(values,[np.append(mid,[angle])],axis=0)
    return values

def perform_3sig(data,s1,hd):
<<<<<<< HEAD
	edges = {}
	size = len(data.keys())
	for num in range(1,int(size/2+1)):
		detect = ef(s1,hd,data['L'+str(num)])
		index_edg = detect.abnormal
		if not np.isnan(index_edg):
			
			detect2 = ef(s1,hd,data['L'+str((size+1-num))])
			index_edg2 = detect.abnormal
			if not np.isnan(index_edg2) :
				edges['L'+str((size+1-num))] = index_edg2
				edges['L'+str(num)] = index_edg
		if len(edges.keys()) >= 4 : break
	return edges
=======
    edges = {}
    size = len(data.keys())
    for num in range(1,int(size/2+1)):
        detect = ef(s1,hd,data['L'+str(num)])
        index_edg = detect.abnormal
        if not np.isnan(index_edg): 
            detect2 = ef(s1,hd,data['L'+str((size+1-num))])
            index_edg2 = detect2.abnormal
            if not np.isnan(index_edg2):
                edges['L'+str(num)] = index_edg
                edges['L'+str((size+1-num))] = index_edg2
        if len(edges.keys()) >= 4 : break 
    return edges
>>>>>>> 47c6ef3100bad6a57c5ee9fda355b19fcfc9c66d

def retrieve_angle(s1,hd,img_path,frame):
    data = frame.get_data(img_path,1) #remove coordinate
    edges = perform_3sig(data,s1,hd)
    print(edges)
<<<<<<< HEAD
    #points = np.empty((0,2),float)
=======
    points = np.empty((0,2),float)
>>>>>>> 47c6ef3100bad6a57c5ee9fda355b19fcfc9c66d
    #print(points)
    #for key in edges.keys():
    #    if np.isnan(edges[key]):
    #        cord = [np.NaN,np.NaN]
    #    else:
    #        cord = frame.lines_frame[key][edges[key]]
            #print('found')
    #    points = np.append(points,[cord],axis=0)
    #print(points)
    #mid_points = mid_angle(points,frame.width,frame.height)
    #return mid_points[:,2]
