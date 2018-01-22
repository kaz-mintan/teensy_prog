# coding:utf-8

import numpy as np
import sys
import math

type_face = 5
num_face = 5
num_ir = 5

# reward function
def calc_reward(state, state_predict, state_before, time_window, mode):
    # coefficient

    c = np.array([0,70.0,70.0,-70.0,-70.0]) #for delta mode
    h = np.array([0,70.0,70.0,-70.0,-70.0]) #for heuristic mode
    reward = 0

    # extract face array (must be time sequence data)
    face = state[0:num_face,:] #in numpy, the 5 of the 0:5 is not included
    face_before = state_before[0:num_face,:]
    #face_before = state[0:num_face,:]
    #face_post = face[:,1:] #for delta mode
    face_predict = state_predict[0:num_face,:] #for predict mode
    #print('sequence.py/face and face_before',face,face_before)


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

def seq2feature(state_mean, state, ir_no,type_face):
    state = state/100.0
    state_feature = np.zeros_like(state_mean)
    state_feature[:type_face] = np.max(state[:type_face],axis=1)*np.mean(state[:type_face], axis=1)

    state_feature[-2]=ir_no
    state_feature[-1]=np.random.uniform(0,1)
    return state_feature

if __name__ == "__main__" :
    type_face = 5
    type_ir = 5
    state_ir = 2
    state = np.zeros((type_face+type_ir,5))
    state_ran = np.random.randint(low=0,high=100,size=state.shape)
    print('state_ran',state_ran)

    state_mean = np.zeros((type_face+state_ir,1))
    state_mean = seq2feature(state_mean[:,0],state_ran,1,type_face)
    print('state_mean',state_mean)

    #argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    #time_window = 3
    #mode = argvs[1]
    state_predict = np.random.uniform(low=0,high=1,size=(num_face+num_ir,time_window))
    #print('state_predict',state_predict)

    reward = calc_reward(state, state_predict, time_window, mode)
    print('reward',reward)

    feature_state = seq2feature(state)
    print(feature_state)
