# coding:utf-8
# calculates reward based on recognized facial expression
import numpy as np

num_face = 5
type_face = 5
type_ir = 5

def f(face):
    face_next = face[:,1:] #for delta mode
    print(face_next-face[:,:face.shape[1]-1])
    do_sum = np.sum(face_next-face[:,:face.shape[1]-1],axis=1)

    return do_sum

def g(face):
    amp_sum = np.sum(face - np.ones_like(face)*0.5,axis=1)
    return amp_sum

def reward_function(state, state_predict, state_before, mode):
    # coefficient
    face = state[0:num_face,:] #in numpy, the 5 of the 0:5 is not included

    c = np.array([0,70.0,70.0,-70.0,-70.0]) #for delta mode
    h = np.array([0,70.0,70.0,-70.0,-70.0]) #for heuristic mode
    reward = 0

    # extract face array (must be time sequence data)
    T_duration = float(face.shape[1])

    return reward

if __name__ == "__main__" :

    state = np.ones((type_face+type_ir,4))
    state_ran = np.random.rand(type_face+type_ir,4)
    print('state_ran',state_ran)
    #state_ran = np.random.rand(5,5)
    print(f(np.array(state_ran[0:num_face,:])))
    print(g(np.array(state_ran[0:num_face,:])))
