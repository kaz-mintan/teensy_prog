# coding:utf-8

import numpy as np
import random

num_face = 5

def type2num(str_type):
    if str_type == 'neutral':
        num = 0
    elif str_type == 'happy':
        num = 1
        num2=2
        num3=4
        num4=3
    elif str_type == 'surprised':
        num = 2
        num2=1
    elif str_type == 'angry':
        num = 3
        num2=4
    elif str_type == 'sad':
        num = 4
        num2=3
        num3=1
        num4=2
    else:
        print('un-registered str')
        num = None
    return num, num2, num3, num4

def get_face(action, target_type, nega_posi, time, time_window):
    # action should be from 0 to 1
    theta = action

    dummy_face = np.zeros(num_face)
    dev = np.zeros(num_face-1)
    dev[0]=0

    num, num2, num3, num4 = type2num(target_type)
    #print('dummy_evaluator.py/time,time_window',theta,0.5*time/time_window+0.5)

    if nega_posi == 'posi':
        dummy_face[num]=(0.80 * theta)#+np.random.uniform(low=-0.05,high=0.05,size=1)
        dummy_face[num2]=(0.10 * theta)
        dummy_face[num3]=(-0.80 * theta + 0.8)
        dummy_face[num4]=(-0.10 * theta + 0.1)
        #print('dummy/dummy_face',dummy_face[num])
    elif nega_posi == 'nega':
        dummy_face[num3]=(0.80 * theta)#+np.random.uniform(low=-0.05,high=0.05,size=1)
        dummy_face[num4]=(0.10 * theta)
        dummy_face[num]=(-0.80 * theta + 0.8)
        dummy_face[num2]=(-0.10 * theta + 0.1)
 
    dummy_face[0]=0.1
    '''
    if nega_posi == 'posi':
        dummy_face[num]=(0.85 * theta+0.1)#+np.random.uniform(low=-0.05,high=0.05,size=1)
        #print('dummy/dummy_face',dummy_face[num])
    elif nega_posi == 'nega':
        dummy_face[num]=(-0.85 * theta+0.95)#+np.random.uniform(low=-0.05,high=0.05,size=1)

    #print('dummy_evaluator.py/dummy_face[num]',dummy_face[num])
    dummy_face[num2] = (1.0 - dummy_face[num])/2.0
    remainning = 1.0 - dummy_face[num] - dummy_face[num2]
    if int(remainning*100) > num_face-2 :
        dev[1:]=random.sample(xrange(int(remainning*100)),num_face-2)
        dev_sort = np.sort(dev)

        t = 0
        for i in range(num_face):
            if i!=num and i!=num2:
                dummy_face[i]=(dev_sort[t+1]-dev_sort[t])/100.0
                t+=1
    '''

    return dummy_face

if __name__ == '__main__':

    face = np.zeros((100,5))
    for theta in range(100):
        face[theta,:]=get_face(theta/100.0,'happy','posi',10,10)
    #print(face)
    np.savetxt('face.csv',face,fmt="%.5f",delimiter=",")
