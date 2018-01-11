# coding:utf-8

import numpy as np

def assumed_z(present_z, limit_max, limit_min):
    array_size = 1
    assumed_dz = np.random.uniform(low=-0.01,high=0.01,size=array_size)
    assumed_z = assumed_dz + present_z
    if assumed_z > limit_max:
        assumed_z = assumed_z - assumed_dz
    elif assumed_z < limit_min:
        assumed_z = assumed_z - assumed_dz

    return assumed_z

def get_ir(present_z):
    limit_max=1
    limit_min=0
    z = assumed_z(present_z,limit_max,limit_min)
    return z

if __name__ == '__main__':
    loop_val = 100
    z_depth = 0
    zlimit_max = 1
    zlimit_min = 0
    z=np.zeros(loop_val)
    for i in range(loop_val):
        z[i]=z_depth
        z_depth = assumed_z(z_depth,zlimit_max,zlimit_min)

    np.savetxt('test_trajectory.csv',z,delimiter=',')
