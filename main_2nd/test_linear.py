# coding:utf-8
import numpy as np
import math

type_ir = 5

def atan(a):
    val = float(a)
    return math.atan(val)*2/math.pi

def linear_state(single_state):
    #print('line/single_state',single_state.shape[0])
    #print('line/single_state',single_state.shape[1])
    a = np.zeros((single_state.shape[0],1))
    for i in range(single_state.shape[1]):
        x = np.linspace(0,1,single_state[i,:].shape[0])
        #fitting
        b, c = np.polyfit(x, single_state[i,:], 1)
        #fitting line
        a[i,0] = atan(b)

    return a
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
    print('input a to test atan')
    a = raw_input()
    print(atan(a))

    type_face = 5
    type_ir = 5

    state = np.random.rand((type_face+type_ir,5))
    #state = np.zeros((type_face+type_ir,5))
    print(linear_state(state))

