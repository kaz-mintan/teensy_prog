# coding:utf-8
# calculates reward based on recognized facial expression
import numpy as np

num_face = 5
type_face = 5
type_ir = 5

def f(face):
    face_next = face[:,1:] #for delta mode
    print('face',face)
    print('face_pots',face_post)
    print(face_next-face[:,:face.shape[1]-1])
    do_sum = np.sum(face_next-face[:,:face.shape[1]-1],axis=1)

    return do_sum

def g(face):
    amp_sum = np.sum(face*0.5 - np.ones_like(face)*0.5)
    return amp_sum

def reward_function(state, state_predict, state_before, mode):
    # coefficient
    face = state[0:num_face,:] #in numpy, the 5 of the 0:5 is not included

    c = np.array([0,70.0,70.0,-70.0,-70.0]) #for delta mode
    h = np.array([0,70.0,70.0,-70.0,-70.0]) #for heuristic mode
    reward = 0

    # extract face array (must be time sequence data)
    T_duration = float(face.shape[1])

    #return sum([x * (num_dizitized**i) for i, x in enumerate(digitized)])
    if mode == 'delta':
        c_face=np.zeros(num_face)
        c_face = np.mean(face,axis=1)-np.mean(face_before,axis=1)
        reward = np.dot(c_face,c)

    elif mode == 'heuristic':
        h_face=np.zeros((num_face,time_window))
        for face_type in range(num_face):
            h_face[face_type,:]=h[face_type]*face[face_type,:]
        reward = np.mean(h_face)

    elif mode == 'predict':
        e_face = face_predict[0,:type_face] - np.mean(face,axis=1)
        print('seq.py/face_predict',face_predict[0,:type_face])
        print('seq.py/face',np.mean(face,axis=1))
        reward = math.fabs(1.0/np.mean(e_face))

    return reward

if __name__ == "__main__" :

    state = np.ones((type_face+type_ir,4))
    state_ran = np.random.rand(type_face+type_ir,4)
    print('state_ran',state_ran)
    #state_ran = np.random.rand(5,5)
    print(f(np.array(state_ran[0:num_face,:])))
