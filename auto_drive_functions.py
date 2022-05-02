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
    print(edges.BND)

    #reducing to points
    allPoints = np.array([frame.fline[i][int(edges.BND[int(i)-1])]for i in frame.fline.keys()])
    points = np.empty([0,2],int)
    for i in range(2,len(edges.BND)-6,2):
        if edges.BND[i] != 0 and edges.BND[i+1]!=0 : 
            points= np.append(points,[frame.fline[str(i+1)][int(edges.BND[i])]],axis=0)
            points= np.append(points,[frame.fline[str(i+2)][int(edges.BND[i+1])]],axis=0)
        if len(points)==6:break
    if len(points) < 3:
        one_side = one_side_check(edges,frame)
        if not np.isnan(np.mean(one_side[0])): return one_side
    # return null if no points found
    if len(points) < 3: return allPoints,np.NaN,np.NaN,np.array([np.NaN]) 
    points[:,1] = 720-points[:,1]
    check = vector_checkV2(points)
    if not np.isnan(check[0]): return allPoints,points,np.NaN,check  #found only one sided
    mid_points = mid_angle(data=points, width=frame.width, height=frame.height) #found two-sides and proceed to calculate angle
    return allPoints, points, mid_points, mid_points[:,2] 

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
                points[:,1] = 720-points[:,1]
                degree = vector_checkV1(points)
                return points,points,np.array([-45,-45]),degree
                break
        if left !=0:
            print(i)
            pleft= np.append(pleft,[frame.fline[str(i+2)][int(left)]],axis=0)
            if len(pleft)==4:
                points = pleft
                points[:,1] = 720-points[:,1]
                degree = vector_checkV1(points)
                return points,points,np.array([45,45]),degree
                break
    return np.NaN,np.NaN,np.NaN


def vector_checkV2(points):
    if len(points[:,0]) >= 4 : 
        vector1 = points[2]-points[0]
        vector2 = points[3]-points[1]
        if (vector1[1] * vector1[0] > 0) and (vector2[1] * vector2[0] > 0) or (vector1[1] * vector1[0] < 0) and (vector2[0] * vector2[1]<0):
            #Should turn Right or right
            radians = np.array([math.atan(vector1[0]/vector1[1]),math.atan(vector2[0]/vector2[1])])
            #return in degree
            return np.degrees(radians)
        else :
            #not a side
            return np.array([np.NaN,np.NaN])
def vector_checkV1(points):
    if len(points[:,0]) >= 4 : 
        vector1 = points[2]-points[0]
        vector2 = points[3]-points[1]
        radians = np.array([math.atan(vector1[0]/vector1[1]),math.atan(vector2[0]/vector2[1])])
        #return in degree
        return np.degrees(radians)
        


def positionCk(Td, Df, Speed):
    carSpeed = (40.2*Speed+3.87)/2.0 #TrueCarSpeed = distance (cm) / 2 Time (s)
    Tt = Df/carSpeed # time of car move in Df distance (cm)
    return Td >= Tt 