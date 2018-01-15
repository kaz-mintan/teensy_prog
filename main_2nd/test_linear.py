# coding:utf-8
import numpy as np
import math

def linear_state(single_state):
    for i in range(single_state.shape[1]):
        print('single_state[:,i]',single_state[:,i])
        print('shape',single_state[:,i].shape[0])
        x = np.linspace(0,1,single_state[:,i].shape[0])
        #fitting
        a, b = np.polyfit(x, single_state, 1)
        #fitting line
    return a

type_face = 5
type_ir = 5
t_window = 4

state = np.zeros((type_face+type_ir,t_window))
state = np.array([[1,1,2],[2,1,3],[5,5,1],[2,2,2]])

#state = np.array([1,1,2,3,1,2,3,3,6,6,4,2,1,2,3,1,2])
print(state)
fh = linear_state(state)
print('fh',fh)
