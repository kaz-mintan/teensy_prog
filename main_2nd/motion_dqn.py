# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
import matplotlib.pyplot as plt
import sys

from sequence import *
from hand_motion import *
from dummy_evaluator import *
from neural_network import *
from datetime import datetime
from serial_pc import *
from save_action_fig import *
from action_dummy import *
from actuate_sma import *

import threading
import thread
from Queue import Queue
import time

select_episode = 50

t_window = 100  #number of time window
num_episodes = 300  #number of all trials

type_face = 5
type_ir = 1
type_action = 1

num_face = 100 #%
num_ir = 100 #5mm
num_action = 100 #%:pwm

gamma = 0.9
alpha = 0.5

epsilon = 0.1
mu = 0.9
epoch = 1000

val_max = 0.8
val_min = 0.2

host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
port = 50000 #クライアントと同じPORTをしてあげます

def nn2q(nn_q):
    return 25.0*nn_q-12.5

def q2nn(q):
    return 0.04*q+0.5

def normalization(array, val_max, val_min):
    x_max = np.max(array)
    x_min = np.min(array)
    a = (val_max - val_min)/(x_max - x_min)
    b = -a*x_max + val_max
    return (a, b)

def inv_normalization(a, b, norm_q):
    return (norm_q - b)/a

def volts(q_teacher, q_k, T=1):
    exp_1=np.sum(np.exp(q_teacher/T))
    exp_2=np.exp(q_k/T)
    return exp_2/exp_1

def select_teach(input_array, q_teacher,episode,num=select_episode):
    index_array = np.argsort(q_teacher)[::-1]
    selected_input = input_array[index_array]
    selected_output = np.sort(q_teacher)[::-1]
    with open('selected_q_index.csv', 'a') as f_handle:
        np.savetxt(f_handle,index_array)

    return selected_input[0,:num,:], selected_output[:,:num]

#5 [4] start main function. set parameters
argvs = sys.argv
target_type = argvs[1]
target_direct = argvs[2]
mode = argvs[3]

# [5] main tourine
state = np.zeros((type_face+type_ir,t_window))
state_before = np.zeros_like(state)
state_predict = np.zeros_like(state)
state_mean = np.zeros((type_face+type_ir,num_episodes))
action = np.zeros((1,num_episodes))
reward = np.zeros(num_episodes)
random = np.zeros(num_episodes)
face_predict = np.zeros((1,type_face))
q_predicted = np.zeros(num_episodes)

state[:,0] = np.array([1,0,0,0,0,0.50])
action[:,0] = np.random.uniform(0,1)

possible_a = np.linspace(0,1,100)

## set qfunction as nn
q_input_size = type_face + type_ir + type_action
q_output_size = 1
q_hidden_size = (q_input_size + q_output_size )/2

q_teacher = np.zeros((q_output_size,num_episodes))

Q_func = Neural(q_input_size, q_hidden_size, q_output_size, epsilon, mu, epoch)
#q_first_iteacher = np.random.uniform(low=0,high=1,size=(q_input_size,1))
#q_first_oteacher = np.random.uniform(low=0,high=0.001,size=(q_output_size,1))

#Q_func.train(q_first_iteacher.T,q_first_oteacher.T)

if mode == 'predict':
    ## set predict function as nn
    p_input_size = type_face + type_ir + type_action
    p_output_size = type_face
    p_hidden_size = (q_input_size + q_output_size )/3

    p_teacher = np.zeros((p_output_size,num_episodes))

    P_func = Neural(p_input_size, p_hidden_size, p_output_size, epsilon, mu, epoch)
    p_first_iteacher = np.random.uniform(low=0,high=1,size=(p_input_size,1))
    p_first_oteacher = np.random.uniform(low=0,high=1,size=(p_output_size,1))

    P_func.train(p_first_iteacher.T,p_first_oteacher.T)

# setting of serial com

ser_port = "/dev/ttyACM0"
ser_baud = 19200
 
get_val = GetSensor(host,port)
sma_act = Serial_com(ser_port,ser_baud)
#sma_act.action(deg)

# main loop
move_flg = 1

for episode in range(num_episodes-1):  #repeat for number of trials
    print('episode',episode,'action',action[:,episode])
    state = np.zeros_like(state_before)
    para_num = 1

    move_flg =1
    #exe_action(100*action[:,episode],para_num)
    deg = 60*action[:,episode]
    sma_act.action(deg)
    state = get_val.get_sensor(t_window)

    #queue=Queue()
    #th_face = threading.Thread(target=get_val.get_sensor,name="th_sma",args=(t_window,queue))
    #th_face.start()


    #print('time',deg/10.0)
    #time.sleep(deg/10.0)
    #print('action finished')

    #for t in range(1,t_window):  #roup for 1 time window
    #th_face.join()
    #state = queue.get()


    ### calcurate s_{t+1} based on the value of sensors
    state_mean[:,episode+1]=seq2feature(state)

    ### calcurate r_{t}
    reward[episode+1] = calc_reward(state, state_predict,
            state_before,t_window, mode)
    print('acted',action[:,episode],'reward',reward[episode+1])

    ### calcurate a_{t+1} based on s_{t+1}
    random_rate = 0.4# * (1 / (episode + 1))
    random[episode+1], action[:,episode+1],next_q = Q_func.gen_action(possible_a,
            num_action, num_face, state_mean, episode,random_rate,action,reward,alpha)

    q_predicted[episode]=next_q
    q_teacher = Q_func.update(state_mean,num_action,num_face,action,episode,q_teacher,reward,next_q, select_episode, gamma, alpha)

    if mode == 'predict':
        state_predict, p_teacher = P_func.predict_update(state_mean,state_predict,num_action,
                num_face,action, episode,p_teacher,reward,next_q,
                select_episode, gamma, alpha)

    before_state = state[:,t_window-1]
    #print('epi',episode,target_type,target_direct,mode,'ran',random[episode],'act',action[:,episode],'rwd',reward[episode+1])

    state_before = state
    print('type',target_type,target_direct,mode)

save_file(num_episodes,action,target_type,target_direct,mode)

np.savetxt('action_pwm.csv', action[0,:], fmt="%.3f", delimiter=",")
np.savetxt('reward_seq.csv', reward, fmt="%.5f",delimiter=",")
np.savetxt('situation.csv', state_mean.T,fmt="%.2f", delimiter=",")
np.savetxt('random_counter.csv', random,fmt="%.0f", delimiter=",")
np.savetxt('q_value.csv', q_teacher,fmt="%.5f", delimiter=",")
np.savetxt('q_predicted.csv', q_predicted,fmt="%.5f", delimiter=",")
