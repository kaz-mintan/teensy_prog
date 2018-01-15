# coding:utf-8
import numpy as np
import math

type_ir = 5

def test_atan(a):
    val = float(a)
    return math.atan(val)*2/math.pi

def linear_state(single_state):
    print('line/single_state',single_state)
    for i in range(single_state.shape[1]):
        x = np.linspace(0,1,single_state[i,:].shape[0])
        #fitting
        a, b = np.polyfit(x, single_state[i,:], 1)
        #fitting line
        a_float = float(a)

    return math.atan(a_float)*2/math.pi
    #return a

def check_thre(ir_sensor,thre):
    ret = -1
    for i in range(type_ir):
        if ir_sensor[i]>thre:
            ret = 1
            break
        else:
            ret = 0
    return ret

if __name__ == '__main__':
    a = raw_input()
    print(test_atan(a))

