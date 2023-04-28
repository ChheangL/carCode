from numba import njit
import numpy as np

#@njit
def false_double_side_check(temp_array,a):
    v1 = temp_array[a-1] - temp_array[a-3]
    v2 = temp_array[a-2] - temp_array[a-4]
    product = (v1[0]/v1[1])*(v2[0]/v2[1])
    if product <= 0:
        return np.array([0.0,0.0])
    else:
        angle1 = np.degrees(np.arctan(v1[0]/v1[1]))
        angle2 = np.degrees(np.arctan(v2[0]/v2[1]))
        return np.array([angle1,angle2])
#@njit
def calculate_mid(temp_array,a):
    mp_1 = (temp_array[1] + temp_array[0])/2.0
    mp_2 = (temp_array[3] + temp_array[2])/2.0
    mp_3 = (temp_array[5] + temp_array[4])/2.0
    a_mp_1 = np.degrees(np.arctan((mp_1[0]-640)/mp_1[1]))
    a_mp_2 = np.degrees(np.arctan((mp_2[0]-640)/mp_2[1]))
    a_mp_3 = np.degrees(np.arctan((mp_3[0]-640)/mp_3[1]))
    return np.array([a_mp_1,a_mp_2,a_mp_3])
#@njit
def calculate_side(array):
    array[:,1] = 720 - array[:,1] 
    empty_arrays = np.zeros_like(array)
    v1 = array[3] - array[0]
    v2 = array[2] - array[1]
    product = (v1[0]/v1[1])*(v2[0]/v2[1])
    if product <= 0:     #Check here : Check product of the slops here and up there
        return empty_arrays
    else:
        empty_arrays[0][0] = np.degrees(np.arctan(v1[0]/v1[1]))
        empty_arrays[0][1] = np.degrees(np.arctan(v2[0]/v2[1]))
        return empty_arrays

#@njit
def single_side_check(temp_arrays):
    right_side = temp_arrays[::2]
    left_side = temp_arrays[1::2]
    a = np.count_nonzero(right_side[:,0])
    b = np.count_nonzero(left_side[:,0])
    if a >= 4:    
        right_side_nZero = np.zeros((a,2))
        i=0
        for n in right_side:
            if not n[0]==0:
                right_side_nZero[i] = n
                i = i + 1
        angle = calculate_side(right_side_nZero)
        return angle,right_side_nZero
    elif b >= 4:
        left_side_nZero = np.zeros((b,2))
        i=0
        for n in left_side:
            if not n[0]==0:
                left_side_nZero[i] = n
                i = i + 1
        angle = calculate_side(left_side_nZero)
        return angle,left_side_nZero
    else:
        empty_array = np.zeros_like(right_side)
        return empty_array,empty_array

#@njit
def get_angle(boundary_points):
    lenght_of_array = len(boundary_points[:,0])
    temp_array = np.zeros_like(boundary_points)
    a = 0
    for n in range(0,lenght_of_array,2):
        if np.mean(boundary_points[n]) and np.mean(boundary_points[n+1]): #check for pairs
            temp_array[a]=boundary_points[n]
            temp_array[a+1] = boundary_points[n+1]
            a = a+2
        if a >= 6:
            #check before calculating mid-points
            temp_array[:a,1] = 720 - temp_array[:a,1] 
            check =  false_double_side_check(temp_array,a)
            if check[0] : 
                return 2,check,temp_array# return the angle and points of the checks
            return 1,calculate_mid(temp_array,a),temp_array
    cp_boundary_points = np.copy(boundary_points)
    a,b= single_side_check(cp_boundary_points)
    if a[0][0]:
        return 3,a[0],b
    else:
        return 4,a[0],b