# coding:utf-8
import numpy as np

def convert_action(action):
    print(action)
    pwm_input = 50*action[0]+10
    keep = 1.5*action[1]+0.2
    delay = 3.0*action[2] + 0.2
    return np.array([pwm_input,keep,delay])

if __name__ == '__main__':
    type_action = 3
    action = np.zeros((type_action,1))
    action[0,0]=1
    action[1,0]=1
    action[2,0]=1
    print(action)
    print(convert_action(action[:,0]))

