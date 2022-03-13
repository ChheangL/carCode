import numpy as np
import math
from ImageFrame import Frame
from EdgeFinderV2 import EdgeFinder as ef


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


def retrieve_angle(s1,h1,hd,layer,img_path,frame):

    data = frame.get_data(img_path,layer) #remove coordinate    
    #print(data)
    edges = ef(data, s1,h1, hd)
    points = np.empty((0,2), float)   
    for key in edges.keys():
        if key == 'side' : break
        if not np.isnan(edges[key]):
            temp = np.flip(frame.lines_frame[key],axis=0)
            cord = temp[edges[key]]
            points = np.append(points, [cord], axis=0)
    if len(edges.keys()) <= 1: return points,np.NaN,np.array([90,90])
    if 'side' in edges.keys():
        if edges['side']==0 : return points,np.NaN,np.array([135,135])
        if edges['side']==1 : return points,np.NaN,np.array([45,45])
    check = vector_check(points)
    if check == 'right': return points,np.NaN,np.array([45,45])
    if check == 'left': return points,np.NaN,np.array([135,135])
        
    mid_points = mid_angle(data=points, width=frame.width, height=frame.height)
    return points, mid_points, mid_points[:,2] 

def vector_check(points):
    if len(points[:,0]) >= 4 : 
        vector1 = points[2]-points[0]
        vector2 = points[3]-points[1]
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        #print(str(norm1)+', '+str(norm2))
        abs_A = math.sqrt(vector1[0]**2 + vector1[1]**2)
        abs_B = math.sqrt(vector2[0]**2 + vector2[1]**2)
        #print(str(abs_A)+', '+str(abs_B))
        #print(vector1)
        #print(vector2)
        D = np.linalg.det([vector2,vector1])
        sin_theta = D/(norm1*norm2)
        print(sin_theta)
        #print(sin_theta)
        if sin_theta <= 0.1 and sin_theta >= -0.1 : 
            if (vector1[1] > 0 and vector1[0] > 0) or (vector1[0] <0 and vector1[1]<0):
                return 'left'
            else:
                return 'right'
        else :
            return 'not a side'
        
    else:
        return np.NaN 