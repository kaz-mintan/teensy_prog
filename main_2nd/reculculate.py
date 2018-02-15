# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
import sys

#from sequence import *
from neural_network import *
from serial_pc import *

import time
from datetime import datetime

from action_convert import *
from reward_calc import *

from test_save_txt import *
from module import *
from sequence import *

argvs = sys.argv
print len(argvs)
if len(argvs)!=4:
    print "(message): input name, mode and day"
else:
    name = argvs[1]
    mode = argvs[2]
    day = argvs[3]

num_episodes = 12  #number of all trials

type_face = 5
type_ir = 5 #5 ir sensors
type_action =3 #3(pwm,delay,num of array)
state_ir = 1 #number of argument of state(ir sensor)

gamma = 0.9
alpha = 0.5

epsilon = 0.1
mu = 0.9
epoch = 1000

#5 [4] start main function. set parameters

path_name = '/home/kumagai/data/waterloo/before/'
dir_name = name + '/exp_201801' +day+'_' + mode + '_' + name +'/'
path = path_name + dir_name

state_file = path+'test_state.csv'
state_mean_file = path+'test_state_mean.csv'
reward_file = path+'test_reward.csv'
action_file = path+'test_action_start.csv'

state_data = np.loadtxt(state_file,delimiter=",")
reward_data = np.loadtxt(reward_file,delimiter=",")
mean_data = np.loadtxt(state_mean_file,delimiter=",")
action_data = np.loadtxt(action_file,delimiter=",")

action_actual=action_data[:,2:5]
#action_actual=np.concatenate(([[0,0,11]],action_org),axis=0)
print('action',action_actual)

reward = np.insert(reward_data[:,1],0,0)
print('reward',reward)
random_rate = 0
inv_action = inv_convert_action(action_actual)

# [5] main tourine
state_mean = np.zeros((type_face+state_ir,num_episodes))
action = np.zeros((type_action,num_episodes))
random = np.zeros(num_episodes)

#initialize action
action[:,0] = np.array([np.random.uniform(0,1),
        np.random.uniform(0,1),
        np.random.uniform(0,1)])
possible_a = np.linspace(0,1,30)

## set qfunction as nn
q_input_size = type_face + state_ir + type_action
q_output_size = 1
q_hidden_size = (q_input_size + q_output_size )/2
q_teacher = np.zeros((q_output_size,num_episodes))
Q_func = Neural(q_input_size, q_hidden_size, q_output_size, epsilon, mu, epoch, gamma, alpha)

p_array= numpy.zeros((q_input_size,1)) #to stock predicted argument
# main loop
for episode in range(num_episodes-1):  #repeat for number of trials
    print('episode',episode)
    state=state_data[np.where(state_data[:,0]==episode),2:2+type_face]
    #print('state',state)
    ir_no = mean_data[episode,6]
    print('ir_no',ir_no)
    state_mean[:,episode] = seq2feature(state_mean[:,episode], state, ir_no,type_face)
    print('state_mean',state_mean[:,episode])

    ### calcurate a_{t} based on s_{t}
    random[episode], action[:,episode], next_q, small_q = Q_func.reculc_gen_action(possible_a, state_mean, episode, random_rate)
    diff_q = next_q - small_q
    ### check q_value of actually selected a_{t}
    print('inv_action',inv_action[:,episode])
    p_array[:,0]=numpy.hstack((state_mean[:,episode+1],inv_action[:,episode]))
    c,actual_q_val = Q_func.predict(p_array.T)
    rate_q = (actual_q_val[0,0]-small_q)/diff_q
    with open('q_check.csv', 'a') as q_handle:
        numpy.savetxt(q_handle,tmp_log(np.hstack((np.array([episode]),np.array(next_q),np.array(small_q),np.array(actual_q_val[0,0]),np.array(diff_q),np.array(rate_q))),datetime.now()),fmt="%.5f",delimiter=",")

    action_array = convert_action(action[:,episode],ir_no)

    #save data of action
    with open('re_action_check.csv', 'a') as act_handle:
        numpy.savetxt(act_handle,tmp_log(np.hstack((np.array([episode]),random[episode],convert_action(action[:,episode],ir_no),action_actual[episode,:])),datetime.now()),fmt="%.3f",delimiter=",")

    q_teacher = Q_func.update(state_mean,inv_action,episode,q_teacher,reward,actual_q_val)
    #q_teacher = Q_func.update(state_mean,inv_convert_action(action_actual),episode-1,q_teacher,reward,actual_q_val)
