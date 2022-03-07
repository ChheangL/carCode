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

def perform_3sigV3(data,s1,h1,hd,sense):
    """version 3 : prioritize in the case of detecting one side
        If one side detect edge and other not : note to one side case (one_side += 1)
        If the next detect edge on both side : note to two side case (two_side += 1)
        
        for one side, need to detect on everyline unless two side case detected in ## consequtive time.
        that mean if two_side == ##(to be determind), then one_side case will be ignore 
    """
    edges = {}
    right_point = {}
    left_point = {}
    size = len(data.keys())
    one_side_left = 0
    one_side_right = 0
    two_side = 0
    num = 2 # the number for two side case to constitude the result
    for num in range(1,int(size/2+1)):
        #check the left side
        detect = ef(s1,h1,hd,data['L'+str(num)],sense)
        index_edg = detect.abnormal['num']
        #print(index_edg)
        detect2 = ef(s1,h1,hd,data['L'+str((size+1-num))],sense)
        index_edg2 = detect2.abnormal['num']
        #print(index_edg2)
        if np.isnan(index_edg) and not np.isnan(index_edg2):
            one_side_right = one_side_right+ 1
            right_point['L'+str((size+1-num))] = index_edg2
            edges = {}
        elif np.isnan(index_edg2) and not np.isnan(index_edg):
            one_side_left = one_side_left + 1

            left_point['L'+str(num)] = index_edg            
            edges = {}
        elif not np.isnan(index_edg) and not np.isnan(index_edg): # found an edge on left side 
            edges['L'+str(num)] = index_edg
            edges['L'+str((size+1-num))] = index_edg2
            two_side = two_side + 1  
            

        if len(edges.keys()) >= 4 or one_side_left >=4 or one_side_right >=4 : break 
    #print(edges)
    #print(left_point)
    #print(one_side_left)
    #print(right_point)
    #print(one_side_right)
    if len(edges.keys())>=4 : return edges
    if one_side_left >= one_side_right : 
        left_point['side'] = 0 #indicating the left
        return left_point
    elif one_side_left <= one_side_right :
        right_point['side'] = 1 #indicating the right        
        return right_point
    else:
        return np.NaN

def perform_3sig(data,s1,h1,hd,sense):
    edges = {}
    size = len(data.keys())
    for num in range(1,int(size/2)):
        detect = ef(s1,h1,hd,data['L'+str(num)],sense)
        index_edg = detect.abnormal['num']
        #print(index_edg)
        detect2 = ef(s1,h1,hd,data['L'+str((size+1-num))],sense)
        index_edg2 = detect2.abnormal['num']
        #print(index_edg2)
        edges['L'+str(num)] = index_edg
        edges['L'+str((size+1-num))] = index_edg2
        #if len(edges.keys()) >= 4 : break 
    return edges  

def retrieve_angle(s1,h1,hd,layer,img_path,frame,sense = 1):

    data = frame.get_data(img_path,layer) #remove coordinate    
    #print(data)
    edges = perform_3sigV3(data, s1,h1, hd,sense)
    print("edges: ", edges)  
    points = np.empty((0,2), float)   
    for key in edges.keys():
        if key == 'side' : break
        if not np.isnan(edges[key]):
            temp = np.flip(frame.lines_frame[key],axis=0)
            cord = temp[edges[key]]
#             print('\nfound!')
#             print("cord: ", cord)
            points = np.append(points, [cord], axis=0)
    #print("\npoints: \n", points)
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