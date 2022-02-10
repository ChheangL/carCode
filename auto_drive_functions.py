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

def perform_3sigV3(data,s1,hd):
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
        detect = ef(s1,hd,data['L'+str(num)])
        index_edg = detect.abnormal
        print(index_edg)
        detect2 = ef(s1,hd,data['L'+str((size+1-num))])
        index_edg2 = detect2.abnormal
        print(index_edg2)
        if np.isnan(index_edg) and not np.isnan(index_edg2):
            one_side_right = one_side_left+ 1

            right_point['L'+str(num)] = index_edg2
            edges = {}
        elif np.isnan(index_edg2) and not np.isnan(index_edg):
            one_side_left = one_side_left + 1

            left_point['L'+str((size+1-num))] = index_edg            
            edges = {}
        elif not np.isnan(index_edg) and not np.isnan(index_edg): # found an edge on left side 
            edges['L'+str(num)] = index_edg
            edges['L'+str((size+1-num))] = index_edg2
            two_side = two_side + 1  
            

        if len(edges.keys()) >= 4 or one_side_left >=4 or one_side_right >=4 : break 
    if len(edges.keys())>=4 : return edges
    if one_side_left >= one_side_right : 
        left_point['side'] = 0 #indicating the left
        return left_point
    elif one_side_left <= one_side_right :
        right_point['side'] = 1 #indicating the right        
        return right_point
    else:
        return np.NaN

def perform_3sig(data,s1,hd):
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

def retrieve_angle(s1,hd,img_path,frame):

    data = frame.get_data(img_path, 1) #remove coordinate
#     print("data: ", data)
    
    edges = perform_3sigV3(data, s1, hd)
    print("edges: ", edges)
#     print("==========================================================")
    
    points = np.empty((0,2), float)
    if 'side' in edges.keys():
        if edges['side']==0 : return np.array([45,45])
        if edges['side']==1 : return np.array([135,135])
    for key in edges.keys():
        if not np.isnan(edges[key]):
            temp = np.flip(frame.lines_frame[key],axis=0)
            cord = temp[edges[key]]
#             print('\nfound!')
#             print("cord: ", cord)
        points = np.append(points, [cord], axis=0)
        
    print("\npoints: \n", points)
        
    mid_points = mid_angle(data=points, width=frame.width, height=frame.height)
    
#     print("\nmid_points: ", mid_points)
    
    return points, mid_points, mid_points[:,2] # Earlier return angle only

