# coding:utf-8
import numpy as np
from datetime import datetime

def tmp_log(array,now):
    print('array',array)
    print('shape',array.shape)
    log_array = np.empty((1,array.shape[0]+5))
    log_array[0,:array.shape[0]]=array
    log_array[0,array.shape[0]:]=\
            np.array([now.day,now.hour,now.minute,now.second,now.microsecond])
    return log_array

def last_log(array):
    log_array = np.empty((1,array.shape[0]))
    log_array[0,:]=array
    return log_array

if __name__ == "__main__" :
    type_face = 5
    type_ir = 5

    d = datetime.now()
    print(np.array([d]))

    tmp_state = np.zeros((type_face+type_ir,1))
    with open('test_save.csv', 'a') as state_handle:
        np.savetxt(state_handle,tmp_log(tmp_state[:,0],d),fmt="%.0f",delimiter=",")
