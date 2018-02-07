# coding:utf-8
import numpy as np

def select_array_num(symm,ir_no):

    array=np.array([[2,2,2],
        [6,8,5],
        [11,14,12],
        [17,20,18],
        [22,22,22]])

    arg_base= int(ir_no)
    symmetry = int(symm)

    print(arg_base,symmetry)
    return array[arg_base,symmetry]

def num2symmetry(num):
    array=np.array([[2,0,0],
        [6,8,5],
        [11,14,12],
        [17,20,18],
        [0,0,22]])

    print(np.where(array == num))
    row, col = np.where(array == num)
    return col

def devide_3(analog_num):
    num = -1
    array=np.linspace(0,1,4)
    if analog_num == 1:
        num = 2
    else:
        for i in range(4):
            if analog_num < array[i] and analog_num>= array[i-1]:
                num = i-1
    return num

def convert_action(action,ir_no):
    pwm_input = int(50*action[0])+35
    #keep = 1.0*action[1]+1.0
    delay = 1.4*action[1] + 0.1
    symmetry = devide_3(action[2])
    base = ir_no
    array_num = select_array_num(symmetry,base)
    return np.array([pwm_input,delay,array_num])

def inv_convert_action(action):
    pwm_row = (action[0]-35.0)/50.0
    delay_row = (action[1]-0.1)/1.4
    symmetry_row = num2symmetry(action[2])


    return np.array([pwm_row, delay_row, symmetry_row])

if __name__ == '__main__':
    num = raw_input()
    print('sym_row',num2symmetry(int(num)))
    type_action = 3
    action = np.zeros((type_action,1))
    action[0,0]=1
    action[1,0]=0.4
    action[2,0]=0.1
    ir_no = 2
    print(convert_action(action[:,0],ir_no))

