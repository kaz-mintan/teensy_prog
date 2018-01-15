# coding:utf-8
import numpy as np
import math

def linear_state(single_state):
    for i in range(single_state.shape[1]):
        x = np.linspace(0,1,single_state[i,:].shape[0])
        #fitting
        a, b = np.polyfit(x, single_state[i,:], 1)
        #fitting line
    return a

