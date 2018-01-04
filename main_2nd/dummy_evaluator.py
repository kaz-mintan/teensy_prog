# coding:utf-8

import numpy as np
import random

num_face = 5

def type2num(str_type):
    if str_type == 'neutral':
        num = 0
    elif str_type == 'happy':
        num = 1
    elif str_type == 'surprised':
        num = 2
    elif str_type == 'angry':
        num = 3
    elif str_type == 'sad':
        num = 4
    else:
        print('un-registered str')
        num = None
    return num

def get_face(action, target_type, nega_posi, time, time_window):
    # action should be from 0 to 1
    theta = action

    dummy_face = np.zeros(num_face)
    dev = np.zeros(num_face)
    dev[0]=0

    num = type2num(target_type)
    #print('dummy_evaluator.py/time,time_window',theta,0.5*time/time_window+0.5)

    if nega_posi == 'posi':
        dummy_face[num]=(0.85 * theta+0.1)+np.random.uniform(low=-0.05,high=0.05,size=1)
        #print('dummy/dummy_face',dummy_face[num])
    elif nega_posi == 'nega':
        dummy_face[num]=(1.0-(0.85 * theta+0.1))+np.random.uniform(low=-0.05,high=0.05,size=1)

    #print('dummy_evaluator.py/dummy_face[num]',dummy_face[num])
    remainning = 1.0 - dummy_face[num]
    if int(remainning*100) > num_face-1 :
        dev[1:]=random.sample(xrange(int(remainning*100)),num_face-1)
        dev_sort = np.sort(dev)

        t = 0
        for i in range(num_face):
            if i!=num:
                dummy_face[i]=(dev_sort[t+1]-dev_sort[t])/100.0
                t+=1

    return dummy_face

if __name__ == '__main__':

    for theta in range(40):
        face=get_face(theta,'happy')
        print(face)

