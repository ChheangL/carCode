import numpy as np
import math
import matplotlib.pyplot as plt
from ImageFrame import Frame
from EdgeFinderV2 import EdgeFinder as ef

previous_angle= np.array([0,0])

def mid_angle(data,width,height):
    data_size = int(len(data))
    values = np.empty((0,3),float)
    for i in range (0, data_size,2):
        mid = (data[i] + data[i+1])/2
        tan = (mid[0]-(width/2.))/(mid[1])
        angle_radiant = math.atan(tan)
        angle_degree = math.degrees(angle_radiant)
        values = np.append(values,[np.append(mid,[angle_degree])],axis=0)
    print(values)
    return values

def retrieve_angle(s1,h1,hd,layer,img_data,frame):

    data = frame.get_data(img_data,layer) #select the data    
    edges = ef(s1,h1, hd,data) #calculate the Boundary
    print(edges.BND)
    #Covert eges.BND to the x-y coordinates
    allPoints = np.array([frame.fline[i][int(edges.BND[int(i)-1])]for i in frame.fline.keys()])
    
    #Determining the case:
    
    #case 1# both sides have boundary for 2nd - 4th pairs
    # if after loop point is empty or not enough points = break
    points = np.empty([0,2],int)
    for i in range(0,len(edges.BND),2):
        if edges.BND[i] != 0 and edges.BND[i+1]!=0 : 
            points= np.append(points,[frame.fline[str(i+1)][int(edges.BND[i])]],axis=0)
            points= np.append(points,[frame.fline[str(i+2)][int(edges.BND[i+1])]],axis=0)
        if len(points)==6:break
    #case 2# one side /return degree
    # if the points converted is less than 3 then one side case is use    
    if len(points) < 3:
        one_side = one_side_check(edges,frame)
        if not np.isnan(one_side[0]):
            print("One side detected")
            return one_side, allPoints,points
    
    # return null if no points found
    if len(points) < 3: return np.array([np.NaN]), allPoints,points
    
    #case 3# one side but detected as two side
    check = vector_checkV2(points)
    if not np.isnan(check[0]): return check, allPoints,points  #found only one sided
    
    #completeing case 1# calculating the degree
    mid_points = mid_angle(data=points, width=frame.width, height=frame.height) #found two-sides and proceed to calculate angle
    global previous_angle 
    previous_angle = mid_points[:,2] #save to previous angle to use when angle are not found
    print("Both side found")
    return previous_angle,allPoints,points

def one_side_check(edges,frame):
    pright = np.empty([0,2],int)
    pleft = np.empty([0,2],int)
    for i in range(0,len(edges.BND),2):
        right = edges.BND[i]
        left = edges.BND[i+1]
        if right !=0:
            pright = np.append(pright,[frame.fline[str(i+1)][int(right)]],axis=0)
            if len(pright)==4:
                points = pright
                degree = vector_checkV1(points)
                return degree
                break
        if left !=0:
            print(i)
            pleft= np.append(pleft,[frame.fline[str(i+2)][int(left)]],axis=0)
            if len(pleft)==4:
                points = pleft
                degree = vector_checkV1(points)
                return degree
                break
    return [np.NaN,np.NaN]

def vector_checkV2(points):
    if len(points[:,0]) >= 4 :
        global previous_angle
        points[:,1] = 720- points[:,1]
        vector1 = points[2]-points[0]
        vector2 = points[3]-points[1]
        if (vector1[1] * vector1[0] > 0) and (vector2[1] * vector2[0] > 0) or (vector1[1] * vector1[0] < 0) and (vector2[0] * vector2[1]<0):
            #Should turn Right or right
            radians = np.array([math.atan(vector1[0]/vector1[1]),math.atan(vector2[0]/vector2[1])])
            #return in degree
            print("Vector Check2 : ", previous_angle)
            previous_angle= np.degrees(radians)
            return previous_angle
        else :
            #not a side
            return np.array([np.NaN,np.NaN])
def vector_checkV1(points):
    if len(points[:,0]) >= 4 :
        global previous_angle
        if point_CHK(points):
            points[:,1] = 720-points[:,1]
            vector1 = points[2]-points[0]
            vector2 = points[3]-points[1]
            radians = np.array([math.atan(vector1[0]/vector1[1]),math.atan(vector2[0]/vector2[1])])
            #return in degree
            print("pointCHK passed : ",previous_angle)
            previous_angle= np.degrees(radians)
        else: 
            print("pointCHK failed : ",previous_angle)
        return previous_angle
    
        
def point_CHK(points):
    v12 = points[1]-points[0]
    v13 = points[2]-points[0]
    v14 = points[3]-points[0]
    v23 = points[2]-points[1]
    v24 = points[3]-points[1]
    v34 = points[3]-points[2]
    dr12 = v12[0]*v12[1]>0
    dr13 = v13[0]*v13[1]>0
    dr14 = v14[0]*v14[1]>0
    dr23 = v23[0]*v23[1]>0
    dr24 = v24[0]*v24[1]>0
    dr34 = v34[0]*v34[1]>0

    dir_points1 = (dr12 and dr13 and dr14)
    dir_points2 = (dr23 and dr24)
    dir_points3 = (dr34)

    #dir_points3 = (v13[0]>0 and v23[0]>0 and v34[0]>0) or (v13[0]<0 and v23[0]<0 and v34[0]<0)
    #dir_points4 = (v14[0]>0 and v24[0]>0 and v34[0]>0) or (v14[0]<0 and v24[0]<0 and v34[0]<0)
    #dir_points1 = (v12[0]>0 and v13[0]>0 and v14[0]>0) or (v12[0]<0 and v13[0]<0 and v14[0]<0)

    return (dir_points1 and dir_points2 and dir_points3) or (not dir_points1 and not dir_points2 and not dir_points3)