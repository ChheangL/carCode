import numpy as np
import math
from ImageFrame import Frame
from EdgeFinder import EdgeFinder as ef


def mid_angle(data,width,height):
    total_point = int(len(data))
    data_per_side = int(total_point/2)
    values = np.empty((0,3),float)
    for i in range (0, data_per_side):
        if np.isnan(data[i][0]) or np.isnan(data[-(i+1)][0]):
            continue
        else:
            mid = (data[i] + data[-(i+1)])/2
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
    edges = {}
    for key in data.keys():
        detect = ef(s1,hd,data[key])
        #if 'num' in detect.abnormal.keys():
        index_edg = detect.abnormal
        edges[key] = index_edg
        #else:
            #edges[key]= np.NaN
    return edges

def retrieve_angle(s1,hd,img_path,frame):
    data = frame.get_data(img_path,1) #remove coordinate
    edges = perform_3sig(data,s1,hd)
    #print(edges)
    points = np.empty((0,2),float)
    #print(points)
    for key in edges.keys():
        if np.isnan(edges[key]):
            cord = [np.NaN,np.NaN]
        else:
            cord = frame.lines_frame[key][edges[key]]
            #print('found')
        points = np.append(points,[cord],axis=0)
    #print(mids_point[:,2])
    mid_points = mid_angle(points,frame.width,frame.height)
    return mid_points[:,2]
