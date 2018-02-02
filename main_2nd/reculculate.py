# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
import sys

#from sequence import *
from neural_network import *
from serial_pc import *

#from get_face_ir import *
#from serial_com import serial_sma
#from serial_com import send_4para

import time
from datetime import datetime

#for test
#from dummy_modules import dummy_evaluator
#from dummy_modules import hand_motion
#from test_linear import *

#from save_files import *
#from datetime import datetime

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
state_ir = 2 #number of argument of state(ir sensor)

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
tmp_time= np.zeros((num_timestamp,1))
dt_array=np.zeros((1,1))
tmp_dt=np.zeros((1,1))

state_mean = np.zeros((type_face+state_ir,num_episodes))
state_reward = np.zeros((type_face+type_ir,1))
time_reward = np.zeros((num_timestamp,1))

time_reward_delay = np.zeros((num_timestamp,1))
dt_array_delay = np.zeros((1,1))
state_reward_delay = np.zeros((type_face+type_ir,1))

stamp_reward = np.zeros((num_episodes-1,2,num_timestamp+1))

state_before = np.zeros_like(state) #for delta mode
state_predict = np.zeros_like((state)) #for predict mode

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

# setting of serial com
get_val = Get_state(ser_port_ir,ser_baud,soc_host,soc_port)
sma_act = send_4para.Act_sma(ser_port_sma,ser_baud)

start_time = 50
wait_cycle = 5

#start to output sensor data
for st in range(start_time):
    print(get_val.ret_state())

# main loop
for episode in range(num_episodes-1):  #repeat for number of trials
    ##########################################################################
    ### detect face and ir to decide action
    ##########################################################################
    state = np.zeros((type_face+type_ir,1))
    state_reward = np.zeros((type_face+type_ir,1))
    state_reward_delay = np.zeros((type_face+type_ir,1))
    time_reward = np.zeros((num_timestamp,1))
    time_reward_delay = np.zeros((num_timestamp,1))
    dt_array_delay = np.zeros((1,1))

    wait = True
    thre = 0.01*10

    start_time_state = datetime.now()
    random_action_time = 5#second

    while_t = 1
    while wait:
        now_time_state = datetime.now()
        delta_time_state = now_time_state - start_time_state

        tmp_state[:,0] = extract_state(get_val.ret_state())#changed to extract

        print('fase/ir as state',tmp_state[:,0])
        with open('test_state.csv', 'a') as rf_handle:
            numpy.savetxt(rf_handle,
                    tmp_log(np.hstack((np.array([episode]),
                        np.array([while_t]),
                        tmp_state[:,0])),datetime.now()),fmt="%f",delimiter=",")

        state=np.hstack((state,tmp_state))
        ir_no, ret = check_thre(np.array(state[type_face:type_ir+type_face,while_t]),thre)

        if ret ==1 and while_t > wait_cycle:
            wait = False
            random_rate = 0
        elif delta_time_state.total_seconds()>random_action_time:
            wait = False
            random_rate = 1
        else:
            while_t += 1

    # if the sensor is larger than the value of threshold, sma starts to move
    state_mean[:,episode] = seq2feature(state_mean[:,episode], state, ir_no,type_face)#TODO
    #TODO waiting

    with open('test_state_mean.csv', 'a') as smean_handle:
        numpy.savetxt(smean_handle,tmp_log(np.hstack((np.array([episode]),state_mean[:,episode])),datetime.now()),fmt="%.3f",delimiter=",")

    ### calcurate a_{t} based on s_{t}
    random[episode], action[:,episode], next_q = Q_func.test_gen_action(possible_a, state_mean, episode, random_rate)

    print('action',(convert_action(action[:,episode],ir_no)))
    action_array = convert_action(action[:,episode],ir_no)
    sma_act.send_para(convert_action(action[:,episode],ir_no))

    #save data of action
    with open('test_action_start.csv', 'a') as act_handle:
        numpy.savetxt(act_handle,tmp_log(np.hstack((np.array([episode]),random[episode],convert_action(action[:,episode],ir_no))),datetime.now()),fmt="%.3f",delimiter=",")

    reward_wait= True
    rewhile_t = 1
    start_time = datetime.now()
    reaction_delay_time = 0 #TODO at this point
    action_end_time = 3*4+2#sec
    #action_time = 3*5+action_array[1]*2 + 5#sec
    action_time = 19#sec
    start_dt = time.time()

    while reward_wait:
        now_time = datetime.now()
        delta_time = now_time - start_time
        #########
        # get face
        #########

        tmp_state[:,0], tmp_time[:,0]  = dev_state_time(get_val.ret_state())
        tmp_dt[0,0] = time.time()-start_dt
        #save data to calculate reward all
        with open('test_reward_face.csv', 'a') as rf_handle:
            numpy.savetxt(rf_handle,tmp_log(np.hstack((np.array([episode]),np.array([rewhile_t]),tmp_state[:,0])),datetime.now()),fmt="%.3f",delimiter=",")

        state_reward=np.hstack((state_reward,tmp_state))
        time_reward=np.hstack((time_reward,tmp_time))
        dt_array=np.hstack((dt_array,tmp_dt))

        if delta_time.total_seconds() > reaction_delay_time\
                and delta_time.total_seconds() < action_end_time:
            state_reward_delay=np.hstack((state_reward_delay,tmp_state))
            time_reward_delay=np.hstack((time_reward_delay,tmp_time))
            dt_array_delay=np.hstack((dt_array_delay,tmp_dt))
            print('t',rewhile_t,'time',tmp_time[:,0],'state',tmp_state[:,0])

            with open('reward_extracted.csv', 'a') as rewext_handle:
                numpy.savetxt(rewext_handle,tmp_log(np.hstack((np.array([episode]),np.array([rewhile_t]),tmp_state[:,0])),datetime.now()),fmt="%f",delimiter=",")

        if delta_time.total_seconds() > action_time:

            with open('test_action_stop.csv', 'a') as act_handle:
                numpy.savetxt(act_handle,tmp_log(np.array([episode]),datetime.now()),fmt="%.3f",delimiter=",")
            reward_wait = False
        else:
            rewhile_t+= 1

    #一番Happyの高いタイムスタンプと低いタイムスタンプ, and number of frameを保存
    stamp_reward = save_stamp(stamp_reward, time_reward_delay, state_reward_delay, episode)
    #print('stamp_reward',stamp_reward)

    ### calcurate r_{t}
    reward[episode+1] = reward_function(state_reward_delay, state_predict, state_before, mode, dt_array_delay)
    with open('test_reward.csv', 'a') as reward_handle:
        numpy.savetxt(reward_handle,tmp_log(np.hstack((np.array([episode+1]),reward[episode+1])),datetime.now()),fmt="%.3f",delimiter=",")

    q_teacher = Q_func.update(state_mean,action,episode-1,q_teacher,reward,next_q)

    state_before = state
    time.sleep(1)

#output reward top and bottom 5 timestamps
#print(stamp_reward)
print('reward',reward)
for i in range(1,num_top+1):
    index_h = np.argsort(reward[1:num_episodes-1])[-i]+1
    index_l = np.argsort(reward[1:num_episodes-1])[::-1][-i]+1

    with open('question_picture.csv', 'a') as q_handle:

        np.savetxt(q_handle,
                last_log(np.hstack((np.array([index_h,reward[index_h]]),stamp_reward[index_h,0,:]))),fmt="%d",delimiter=",")

        print(np.hstack((np.array([index_h,reward[index_h]]),stamp_reward[index_h,0,:])))
        print(np.hstack((np.array([index_l,reward[index_l]]),stamp_reward[index_l,1,:])))
        np.savetxt(q_handle,
                last_log(np.hstack((np.array([index_l,reward[index_l]]),stamp_reward[index_l,1,:]))),fmt="%d",delimiter=",")

#reward[n]の値が最も高いインデックスiを5つ見つけて、stamp_reward[i,0,:]をCSVに出力
#reward[n]の値が最も低いインデックスiを5つ見つけて、stamp_reward[i,0,:]をCSVに出力

