# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
import matplotlib.pyplot as plt
import sys

from sequence import *
from neural_network import *
from serial_pc import *

from get_face_ir import *
from serial_com import serial_sma

#import threading
#import thread
#from Queue import Queue
import time
from datetime import datetime

t_window = 100  #number of time window
num_episodes = 300  #number of all trials

type_face = 5
type_ir = 5 #5 ir sensors
type_action = 15 #3(pwm,keep,delay) times 5 sma sensors

gamma = 0.9
alpha = 0.5

epsilon = 0.1
mu = 0.9
epoch = 1000

soc_host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
soc_port = 50000 #クライアントと同じPORTをしてあげます
ser_baud = 19200

#5 [4] start main function. set parameters
argvs = sys.argv
mode = argvs[1]
ser_port_sma = argvs[2]
ser_port_ir = argvs[3]
print('port_sma',ser_port_sma)
print('port_ir',ser_port_ir)

# [5] main tourine
state = np.zeros((type_face+type_ir,t_window))
state_mean = np.zeros((type_face+type_ir,num_episodes))

state_before = np.zeros_like(state) #for delta mode
state_predict = np.zeros_like(state) #for predict mode

action = np.zeros((1,num_episodes))
reward = np.zeros(num_episodes)
random = np.zeros(num_episodes)

face_predict = np.zeros((1,type_face)) #for predict mode
q_predicted = np.zeros(num_episodes)

#state[:,0] = np.array([1,0,0,0,0,0.50])
action[:,0] = np.random.uniform(0,1)

possible_a = np.linspace(0,1,100)

## set qfunction as nn
q_input_size = type_face + type_ir + type_action
q_output_size = 1
q_hidden_size = (q_input_size + q_output_size )/2

q_teacher = np.zeros((q_output_size,num_episodes))

Q_func = Neural(q_input_size, q_hidden_size, q_output_size, epsilon, mu, epoch)

if mode == 'predict':
    ## set predict function as nn
    p_input_size = type_face + type_ir + type_action
    p_output_size = type_face
    p_hidden_size = (p_input_size + p_output_size )/3

    p_teacher = np.zeros((p_output_size,num_episodes))

    P_func = Neural(p_input_size, p_hidden_size, p_output_size, epsilon, mu, epoch)
    p_first_iteacher = np.random.uniform(low=0,high=1,size=(p_input_size,1))
    p_first_oteacher = np.random.uniform(low=0,high=1,size=(p_output_size,1))

    P_func.train(p_first_iteacher.T,p_first_oteacher.T)

# setting of serial com
get_val = Get_state(ser_port_ir,ser_baud,soc_host,soc_port)
sma_act = serial_sma.Act_sma(ser_port_sma,ser_baud)

thre = 10

# main loop
for episode in range(num_episodes-1):  #repeat for number of trials
    print('episode',episode,'action',action[:,episode])
    state = np.zeros_like(state_before)
    para_num = 1

    wait = True
    thre = action[]
    wait_time = action[]

    while wait:
        state[:,t]=get_val.ret_state()#TODO
        if state[:,t]>thre:
            sleep(wait_time)
            wait = False
    # if the sensor is larger than the value of threshold, sma starts to move
    #if state > thre:#TODO decide the val of thre
    deg = 30*action[:,episode]+70
    sma_act.act(deg)
    t_window = action[]に基づき決定する
    for t in range(1,t_window):
        state_reward[:,t] = get_val.ret_state()
        print('state',state[:,t])

    ### calcurate s_{t+1} based on the value of sensors
    state_mean[:,episode+1]=seq2feature(state_reward)

    ### calcurate r_{t}
    reward[episode+1] = calc_reward(state, state_predict,
            state_before,t_window, mode)
    print('acted',action[:,episode],'reward',reward[episode+1])

    ### calcurate a_{t+1} based on s_{t+1}
    random_rate = 0.4# * (1 / (episode + 1))
    random[episode+1], action[:,episode+1],next_q = Q_func.gen_action(possible_a,
            state_mean, episode,random_rate,action,reward,alpha)

    q_predicted[episode]=next_q
    q_teacher = Q_func.update(state_mean,action,episode,q_teacher,reward,next_q, gamma, alpha)

    if mode == 'predict':
        state_predict, p_teacher = P_func.predict_update(state_mean,state_predict,
                action, episode,p_teacher,reward,next_q,
                gamma, alpha)

    #before_state = state[:,t_window-1]
    state_before = state

save_file(num_episodes,action,target_type,target_direct,mode)

np.savetxt('action_pwm.csv', action[0,:], fmt="%.3f", delimiter=",")
np.savetxt('reward_seq.csv', reward, fmt="%.5f",delimiter=",")
np.savetxt('situation.csv', state_mean.T,fmt="%.2f", delimiter=",")
np.savetxt('random_counter.csv', random,fmt="%.0f", delimiter=",")
np.savetxt('q_value.csv', q_teacher,fmt="%.5f", delimiter=",")
np.savetxt('q_predicted.csv', q_predicted,fmt="%.5f", delimiter=",")
