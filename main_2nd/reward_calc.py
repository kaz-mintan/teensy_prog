# coding:utf-8
# calculates reward based on recognized facial expression
import numpy as np
import math
import time

num_face = 5
type_face = 5
type_ir = 5

def f(face,t_array):
    face_next = face[:,1:] #for delta mode
    t_next = t_array[1:]
    do = face_next-face[:,:face.shape[1]-1]
    dt = t_next-t_array[:face.shape[1]-1]
    dt_tile = np.tile(dt,(face.shape[0],1))
    do_sum = np.sum(do/dt,axis=1)

    return do_sum

def g(face):
    #amp_sum = np.sum(face - np.ones_like(face)*50,axis=1)
    amp_sum = np.sum(face,axis=1)
    return amp_sum

def reward_function(state, state_predict, state_before, mode, t_array):
    # extract face array (must be time sequence data)
    face = state[0:num_face,:] #in numpy, the 5 of the 0:5 is not included
    t = t_array[0,:]

    # coefficient
    c_f = np.array([0,3.0,0.0,-1.0,-1.0]) #for delta mode
    c_g = np.array([0,9.0,0.0,-3.0,-3.0]) #for delta mode
    h = np.array([0,70.0,70.0,-70.0,-70.0]) #for heuristic mode

    T_duration = float(face.shape[1])
    #reward = np.sum(c_f*f(face)+c_g*g(face))

    if mode == 'delta':
        reward = np.sum(c_f*f(face,t))

    elif mode == 'heuristic':
        reward = np.sum(c_g*g(face))

    elif mode == 'predict':
        face_predict = state_predict[0:num_face,:] #for predict mode
        e_face = face_predict[0,:type_face] - np.mean(face,axis=1)

        reward = math.fabs(1.0/np.mean(e_face))

    return reward

if __name__ == "__main__" :

    state = np.ones((type_face+type_ir,4))
    state_ran = np.random.rand(type_face+type_ir,4)
    dt_array=np.random.rand(1,4)
    print('dt',dt_array)

    print('state_ran',state_ran)
    #state_ran = np.random.rand(5,5)
    print('f(state)',f(np.array(state_ran[0:num_face,:]),dt_array))
    print('g(state)',g(np.array(state_ran[0:num_face,:])))
    print(reward_function(state_ran,state,state,'heuristic',dt_array))
