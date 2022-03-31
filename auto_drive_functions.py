import numpy as np
import math
from ImageFrame import Frame
from EdgeFinderV2 import EdgeFinder as ef


def mid_angle(data,width,height):
    data_size = int(len(data))
    values = np.empty((0,3),float)
    for i in range (0, data_size,2):
        mid = (data[i] + data[i+1])/2
        tan = (mid[0]-(width/2.))/(height-mid[1])
        angle_radiant = math.atan(tan)
        angle_degree = math.degrees(angle_radiant)
        #print('The degree is {:.2f}'.format(angle_degree))
        #angle = ((-1)*angle_degree if angle_degree < 0 else 180-angle_degree)
        values = np.append(values,[np.append(mid,[angle_degree])],axis=0)
    return values

def retrieve_angle(s1,h1,hd,layer,img_path,frame):

    data = frame.get_data(img_path,layer) #select the data    
    edges = ef(s1,h1, hd,data) #calculate the Boundary
    #reducing only pair points
    allPoints = np.array([frame.fline[i][int(edges.BND[int(i)-1])]for i in frame.fline.keys()])
    points = np.empty([0,2],int)
    for i in range(2,len(edges.BND)-6,2):
        if edges.BND[i] != 0 and edges.BND[i+1]!=0 : 
            points= np.append(points,[frame.fline[str(i+1)][int(edges.BND[i])]],axis=0)
            points= np.append(points,[frame.fline[str(i+2)][int(edges.BND[i+1])]],axis=0)
        if len(points)==6:break
    if len(points) < 3:
        pright = np.empty([0,2],int)
        pleft = np.empty([0,2],int)
        for i in range(0,len(edges.BND),2):
            right = edges.BND[i]
            left = edges.BND[i+1]
            if right !=0:
                pright = np.append(pright,[frame.fline[str(i+1)][int(right)]],axis=0)
                if len(pright)==4: 
                    points = pright
                    return allPoints,points,np.array([-45,-45]),np.array([-45,-45])
                    break
            if left !=0:
                pleft= np.append(pleft,[frame.fline[str(i+2)][int(left)]],axis=0)
                if len(pleft)==4: 
                    points = pleft
                    return allPoints,points,np.array([45,45]),np.array([45,45])
                    break
        
#     print(edges.BND)
    if len(points) < 3: return allPoints,np.NaN,np.NaN,np.array([np.NaN]) 
    check = vector_check(points)
    if check == 'right': return allPoints,points,np.array([-45,-45]),np.array([-45,-45])
    if check == 'left': return allPoints,points,np.array([45,45]),np.array([45,45])
    mid_points = mid_angle(data=points, width=frame.width, height=frame.height)
    return allPoints, points, mid_points, mid_points[:,2] 

def vector_check(points):
    if len(points[:,0]) >= 4 : 
        vector1 = points[2]-points[0]
        vector2 = points[3]-points[1]
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        #abs_A = math.sqrt(vector1[0]**2 + vector1[1]**2) # The code here just to show that it is the same as norm function
        #abs_B = math.sqrt(vector2[0]**2 + vector2[1]**2) #
        D = np.linalg.det([vector2,vector1])
        sin_theta = D/(norm1*norm2)
#         print(sin_theta)
        if sin_theta <= 0.1 and sin_theta >= -0.1 : 
            if (vector1[1] > 0 and vector1[0] > 0) or (vector1[0] <0 and vector1[1]<0):
                return 'right'
            else:
                return 'left'
        else :
            return 'not a side'
        
    else:
        return np.NaN 

