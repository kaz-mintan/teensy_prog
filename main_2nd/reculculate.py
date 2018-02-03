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

num_episodes = 12  #number of all trials
num_top = 2

num_timestamp = 4#hour, minute, second and millisecond
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
argvs = sys.argv
name = argvs[1]
mode = argvs[2]
day = argvs[3]

path_name = '/home/kumagai/data/waterloo/before/'
dir_name = name + '/exp_201801' +day+'_' + mode + '_' + name +'/'
path = path_name + dir_name

state_file = 'test_state.csv'
state_mean_file = 'test_state_mean.csv'
reward_face_file = 'test_reward_face.csv'

state_data = np.loadtxt(path+state_file,delimiter=",")
print(path+state_mean_file)
ir_no = np.loadtxt(path+state_mean_file,delimiter=",")
face_data = np.loadtxt(path+reward_face_file,delimiter=",")

# [5] main tourine
#state = np.zeros((type_face+type_ir,1))
#tmp_state = np.zeros((type_face+type_ir,1))
#tmp_time= np.zeros((num_timestamp,1))
#dt_array=np.zeros((1,1))
#tmp_dt=np.zeros((1,1))

state_mean = np.zeros((type_face+state_ir,num_episodes))
state_reward = np.zeros((type_face+type_ir,1))
time_reward = np.zeros((num_timestamp,1))

time_reward_delay = np.zeros((num_timestamp,1))
dt_array_delay = np.zeros((1,1))
state_reward_delay = np.zeros((type_face+type_ir,1))

stamp_reward = np.zeros((num_episodes-1,2,num_timestamp+1))

#state_before = np.zeros_like(state) #for delta mode
#state_predict = np.zeros_like((state)) #for predict mode

action = np.zeros((type_action,num_episodes))
reward = np.zeros(num_episodes+1)
random = np.zeros(num_episodes)

#initialize action

action[:,0] = np.array([np.random.uniform(0,1),
        np.random.uniform(0,1),
        np.random.uniform(0,1)])
possible_a = np.linspace(0,1,20)

## set qfunction as nn
q_input_size = type_face + state_ir + type_action
q_output_size = 1
q_hidden_size = (q_input_size + q_output_size )/2
q_teacher = np.zeros((q_output_size,num_episodes))
Q_func = Neural(q_input_size, q_hidden_size, q_output_size, epsilon, mu, epoch, gamma, alpha)

start_time = 50
wait_cycle = 5

# main loop
for episode in range(num_episodes-1):  #repeat for number of trials
    ##########################################################################
    ### detect face and ir to decide action
    ##########################################################################
    #state = np.zeros((type_face+type_ir,1))
    #state_reward = np.zeros((type_face+type_ir,1))
    #state_reward_delay = np.zeros((type_face+type_ir,1))
    #time_reward = np.zeros((num_timestamp,1))
    #time_reward_delay = np.zeros((num_timestamp,1))
    #dt_array_delay = np.zeros((1,1))

    state=state_data[np.where(state_data[:,0]==0),2:2+type_face]
    ir_no = np.loadtxt(state_mean_file)
    state_mean[:,episode] = seq2feature(state_mean[:,episode], state, ir_no,type_face)

    ### calcurate a_{t} based on s_{t}
    random[episode], action[:,episode], next_q = Q_func.test_gen_action(possible_a, state_mean, episode, random_rate)

    print('action',(convert_action(action[:,episode],ir_no)))
    action_array = convert_action(action[:,episode],ir_no)
    #TODO change: write test_action.csv(no change?)

    #save data of action
    with open('re_action.csv', 'a') as act_handle:
        numpy.savetxt(act_handle,tmp_log(np.hstack((np.array([episode]),random[episode],convert_action(action[:,episode],ir_no))),datetime.now()),fmt="%.3f",delimiter=",")

    reward_wait= True
    rewhile_t = 1
    start_time = datetime.now()
    reaction_delay_time = 0
    action_end_time = 3*4+2#sec
    action_time = 19#sec
    start_dt = time.time()

    while reward_wait:
        now_time = datetime.now()
        delta_time = now_time - start_time

        #TODO change: read test_reward_face.csv
        tmp_state[:,0], tmp_time[:,0]  = np.loadtxt(reward_file)
        tmp_dt[0,0] = time.time()-start_dt
        #save data to calculate reward all

        if delta_time.total_seconds() > reaction_delay_time\
                and delta_time.total_seconds() < action_end_time:
            state_reward_delay=np.hstack((state_reward_delay,tmp_state))
            time_reward_delay=np.hstack((time_reward_delay,tmp_time))
            dt_array_delay=np.hstack((dt_array_delay,tmp_dt))
            print('t',rewhile_t,'time',tmp_time[:,0],'state',tmp_state[:,0])

        if delta_time.total_seconds() > action_time:
            reward_wait = False
        else:
            rewhile_t+= 1

    ### calcurate r_{t}
    reward[episode+1] = reward_function(state_reward_delay, state_predict, state_before, mode, dt_array_delay)

    q_teacher = Q_func.update(state_mean,action,episode-1,q_teacher,reward,next_q)

    state_before = state
    time.sleep(1)
