# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
import matplotlib.pyplot as plt
import sys

#from sequence import *
from neural_network import *
from serial_pc import *

from get_face_ir import *
from serial_com import serial_sma
from serial_com import send_3para

import time
from datetime import datetime

#for test
from dummy_modules import dummy_evaluator
from dummy_modules import hand_motion
from test_linear import *

from save_files import *
from datetime import datetime

from action_convert import *
from reward_calc import *

from test_save_txt import *

t_window = 10  #number of time window
num_episodes = 50  #number of all trials

type_face = 5
type_ir = 5 #5 ir sensors
type_action = 3 #3(pwm,keep,delay) times 5 sma sensors

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
state = np.zeros((type_face+type_ir,1))
tmp_state = np.zeros((type_face+type_ir,1))
state_mean = np.zeros((type_face+type_ir,num_episodes))
state_reward = np.zeros((type_face+type_ir,1))
state_reward_delay = np.zeros((type_face+type_ir,1))

state_before = np.zeros_like(state) #for delta mode
state_predict = np.zeros_like(state) #for predict mode

action = np.zeros((type_action,num_episodes))
reward = np.zeros(num_episodes)
random = np.zeros(num_episodes)

#initialize action
action[:,0] = np.array([np.random.uniform(0,1),np.random.uniform(0,1),np.random.uniform(0,1)])
possible_a = np.linspace(0,1,10)
print('shape',possible_a.shape[0])

## set qfunction as nn
q_input_size = type_face + type_ir + type_action
q_output_size = 1
q_hidden_size = (q_input_size + q_output_size )/2
q_teacher = np.zeros((q_output_size,num_episodes))
Q_func = Neural(q_input_size, q_hidden_size, q_output_size, epsilon, mu, epoch, gamma, alpha)

if mode == 'predict':
    ## set predict function as nn
    p_input_size = type_face + type_ir + type_action
    p_output_size = type_face
    p_hidden_size = (p_input_size + p_output_size )/3

    p_teacher = np.zeros((p_output_size,num_episodes))

    P_func = Neural(p_input_size, p_hidden_size, p_output_size, epsilon, mu, epoch,gamma, alpha)
    p_first_iteacher = np.random.uniform(low=0,high=1,size=(p_input_size,1))
    p_first_oteacher = np.random.uniform(low=0,high=1,size=(p_output_size,1))

    P_func.train(p_first_iteacher.T,p_first_oteacher.T)

# setting of serial com
get_val = Get_state(ser_port_ir,ser_baud,soc_host,soc_port)
sma_act = send_3para.Act_sma(ser_port_sma,ser_baud)

#for save files
save_files = Save_csv(datetime.now())

state[:,0]=np.array([0,0,0,0,0,0,0,0,0,0])
state_reward[:,0]=np.array([0,0,0,0,0,0,0,0,0,0])

# main loop
for episode in range(num_episodes-1):  #repeat for number of trials

    state = np.zeros((type_face+type_ir,1))

    wait = True
    thre = 30
    wait_cycle = 5

    while_t = 1
    while wait:
        tmp_state[:,0] = get_val.ret_state()

        print('fase/ir as state',tmp_state[:,0])
        state=np.hstack((state,tmp_state))

        if check_thre(np.array(state[type_face:type_ir+type_face,while_t]),thre)==1 and while_t > wait_cycle:
            wait = False
        else:
            while_t += 1

    # if the sensor is larger than the value of threshold, sma starts to move
    state_mean[:,episode] = linear_state(state)#TODO
    with open('test_state_mean.csv', 'a') as smean_handle:
        numpy.savetxt(smean_handle,tmp_log(state_mean[:,episode]),fmt="%.5f",delimiter=",")

    ### calcurate a_{t} based on s_{t}
    random_rate = 0.4# * (1 / (episode + 1))
    random[episode], action[:,episode], next_q = Q_func.test_gen_action(possible_a, state_mean, episode, random_rate)

    with open('test_action.csv', 'a') as act_handle:
        numpy.savetxt(act_handle,tmp_log(np.hstack((random[episode],action[:,episode]))),fmt="%.5f",delimiter=",")

    print('action',(convert_action(action[:,episode])))
    action_array = convert_action(action[:,episode])
    sma_act.send_para(convert_action(action[:,episode]))
    sma_act.send_para(convert_action(action[:,episode]))

    reward_wait= True
    rewhile_t = 1
    start_time = datetime.now()
    reaction_delay_time = 0.5 #TODO at this point
    action_end_time = action_array[1]*4+action_array[2]#sec
    action_time = action_array[1]*5+action_array[2]*2 + 15#sec
    while reward_wait:
        now_time = datetime.now()
        delta_time = now_time - start_time
        #state[:,while_t]=get_val.ret_state()#TODO
        tmp_state[:,0] = get_val.ret_state()
        with open('test_reward_face.csv', 'a') as rf_handle:
            numpy.savetxt(rf_handle,tmp_log(tmp_state[:,0]).T,fmt="%.5f",delimiter=",")

        print('face as reward',tmp_state[:,0])
        state_reward=np.hstack((state_reward,tmp_state))

        if delta_time.total_seconds() > reaction_delay_time\
                and delta_time.total_seconds() < action_end_time:
            state_reward_delay=np.hstack((state_reward_delay,tmp_state))

        if delta_time.total_seconds() > action_time:
            reward_wait = False
        else:
            rewhile_t+= 1

    ### calcurate r_{t}
    reward[episode+1] = reward_function(state_reward_delay, state_predict, state_before, mode)
    #reward[episode+1] = reward_function(state_reward, state_predict, state_before, mode)
    with open('test_reward.csv', 'a') as reward_handle:
        numpy.savetxt(reward_handle,tmp_log(np.hstack((reward[episode+1],np.array([episode+1])))),fmt="%.5f",delimiter=",")

    print('reward',reward[episode+1])

    q_teacher = Q_func.update(state_mean,action,episode-1,q_teacher,reward,next_q)
    #q_teacher = Q_func.update(state_mean,action,episode,q_teacher,reward,next_q, gamma, alpha)

    if mode == 'predict':
        state_predict, p_teacher = P_func.predict_update(state_mean,state_predict,
                action, episode,p_teacher,reward,next_q)
                #action, episode,p_teacher,reward,next_q, gamma, alpha)

    state_before = state
    time.sleep(3)

