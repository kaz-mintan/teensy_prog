# coding:utf-8
import numpy as np
import math

def linear_state(single_state):
    x = np.linspace(0,1,single_state.shape[0])
    #fitting
    a, b = np.polyfit(x, single_state, 1)
    #fitting line
    return a


state = np.array([1,1,2,3,1,2,3,3,6,6,4,2,1,2,3,1,2])
print(state.shape[0])
fh = linear_state(state)
print(fh)
