# coding:utf-8
import numpy as np

def devide_base(analog_base):
    if analog_base>=0 and analog_base<0.2:
        dib_base = 0
    elif analog_base>=0.2 and analog_base<0.4:
        dib_base = 1
    elif analog_base>=0.4 and analog_base<0.6:
        dib_base = 2
    elif analog_base>=0.6 and analog_base<0.8:
        dib_base = 3
    elif analog_base>=0.8 and analog_base<1.0:
        dib_base = 4
    return dig_base

def devide_2(analog_num):
    if analog_num>=0 and analog_num<0.5:
        dib_num = 0
    elif analog_base>=0.5 and analog_base<1.0:
        dib_num= 1
    return dig_num

def convert_action(action):
    pwm_input = 30*action[0]+70
    #keep = 1.0*action[1]+1.0
    delay = 1.5*action[1] + 1.0
    base = devide_base(action[2])
    num = devide_2(action[3])
    direction = devide_2(action[4])
    return np.array([pwm_input,delay,base,num,direction])

if __name__ == '__main__':
    type_action = 3
    action = np.zeros((type_action,1))
    action[0,0]=1
    action[1,0]=1
    action[2,0]=1
    print(action)
    print(convert_action(action[:,0]))

