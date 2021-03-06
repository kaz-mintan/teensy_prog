# coding:utf-8
# http://neuro-educator.com/rl1/

import numpy as np
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
from module import *

t_window = 10  #number of time window
num_episodes = 5  #number of all trials
num_top = 3

num_timestamp = 4#hour, minute, second and millisecond
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
tmp_time= np.zeros((num_timestamp,1))
state_mean = np.zeros((type_face+type_ir,num_episodes))
state_reward = np.zeros((type_face+type_ir,1))
time_reward = np.zeros((num_timestamp,1))
state_reward_delay = np.zeros((type_face+type_ir,1))
stamp_reward = np.zeros((num_episodes+1,2,num_timestamp))

state_before = np.zeros_like(state) #for delta mode
state_predict = np.zeros_like((type_face+type_ir,num_episodes)) #for predict mode

action = np.zeros((type_action,num_episodes))
reward = np.zeros(num_episodes+1)
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

start_time = 100
wait_cycle = 5

#start to output sensor data
for st in range(start_time):
    print(get_val.ret_state())

# main loop
for episode in range(num_episodes-1):  #repeat for number of trials
    #####################################
    # detect face and ir to decide action
    #####################################
    state = np.zeros((type_face+type_ir,1))

    wait = True
    thre = 10

    while_t = 1
    while wait:
        tmp_state[:,0] = extract_state(get_val.ret_state())#changed to extract

        print('fase/ir as state',tmp_state[:,0])
        #TODO state_log
        with open('test_reward_face.csv', 'a') as rf_handle:
            numpy.savetxt(rf_handle,
                    tmp_log(np.hstack((np.array([episode]),
                        np.array([rewhile_t]),
                        tmp_state[:,0]))),fmt="%.5f",delimiter=",")

        state=np.hstack((state,tmp_state))
        if check_thre(np.array(state[type_face:type_ir+type_face,while_t]),thre)==1 and while_t > wait_cycle:
            wait = False
        else:
            while_t += 1

    # if the sensor is larger than the value of threshold, sma starts to move
    state_mean[:,episode] = linear_state(state)#TODO
    with open('test_state_mean.csv', 'a') as smean_handle:
        numpy.savetxt(smean_handle,tmp_log(np.hstack((np.array([episode]),np.array([while_t]),state_mean[:,episode]))),fmt="%.5f",delimiter=",")

    ### calcurate a_{t} based on s_{t}
    random_rate = 0.3# * (1 / (episode + 1))
    random[episode], action[:,episode], next_q = Q_func.test_gen_action(possible_a, state_mean, episode, random_rate)

    with open('test_action.csv', 'a') as act_handle:
        numpy.savetxt(act_handle,tmp_log(np.hstack((np.array([episode]),random[episode],action[:,episode]))),fmt="%.5f",delimiter=",")

    print('action',(convert_action(action[:,episode])))
    action_array = convert_action(action[:,episode])
    sma_act.send_para(convert_action(action[:,episode]))

    reward_wait= True
    rewhile_t = 1
    start_time = datetime.now()
    reaction_delay_time = 0.5 #TODO at this point
    action_end_time = action_array[1]*4+action_array[2]#sec
    action_time = action_array[1]*5+action_array[2]*2 + 7#sec
    while reward_wait:
        now_time = datetime.now()
        delta_time = now_time - start_time
        #check the episode is correct?
        tmp_state[:,0], tmp_time[:,0]  = dev_state_time(get_val.ret_state())
        with open('test_reward_face.csv', 'a') as rf_handle:
            numpy.savetxt(rf_handle,tmp_log(np.hstack((np.array([episode]),np.array([rewhile_t]),tmp_state[:,0]))),fmt="%.5f",delimiter=",")

        print('face as reward',tmp_state[:,0])
        state_reward=np.hstack((state_reward,tmp_state))
        #check the episode is correct?
        time_reward=np.hstack((time_reward,tmp_time))

        if delta_time.total_seconds() > reaction_delay_time\
                and delta_time.total_seconds() < action_end_time:
            state_reward_delay=np.hstack((state_reward_delay,tmp_state))
            with open('reward_extracted.csv', 'a') as rewext_handle:
                #numpy.savetxt(rewext_handle,tmp_log(state_reward_delay[:,episode]),fmt="%.5f",delimiter=",")
                numpy.savetxt(rewext_handle,tmp_log(state_reward_delay[:,rewhile_t]),fmt="%.5f",delimiter=",")

        if delta_time.total_seconds() > action_time:
            reward_wait = False
        else:
            rewhile_t+= 1

    #一番Happyの高いタイムスタンプと低いタイムスタンプを保存
    ### calcurate r_{t}
    stamp_reward = save_stamp(stamp_reward, time_reward, state_reward, episode+1)

    reward[episode+1] = reward_function(state_reward_delay, state_predict, state_before, mode)
    #reward[episode+1] = reward_function(state_reward, state_predict, state_before, mode)
    with open('test_reward.csv', 'a') as reward_handle:
        numpy.savetxt(reward_handle,tmp_log(np.hstack((np.array([episode+1]),reward[episode+1]))),fmt="%.5f",delimiter=",")

    print('reward',reward[episode+1])

    q_teacher = Q_func.update(state_mean,action,episode-1,q_teacher,reward,next_q)
    #q_teacher = Q_func.update(state_mean,action,episode,q_teacher,reward,next_q, gamma, alpha)

    if mode == 'predict':
        state_predict, p_teacher = P_func.predict_update(state_mean,state_predict,
                action, episode,p_teacher,reward,next_q)
                #action, episode,p_teacher,reward,next_q, gamma, alpha)

    state_before = state
    time.sleep(5)

#output reward top and bottom 5 timestamps


for i in range(1,num_top+1):
    with open('question_picture.csv', 'a') as q_handle:
        numpy.savetxt(q_handle,tmp_log(stamp_reward[np.argsort(reward)[-i],0,:]),fmt="%.5f",delimiter=",")
        numpy.savetxt(q_handle,tmp_log(stamp_reward[np.argsort(reward)[i],1,:]),fmt="%.5f",delimiter=",")

    #print(stamp_reward[np.argsort(reward)[-i],0,:])
    #print(stamp_reward[np.argsort(reward)[i],1,:])

#reward[n]の値が最も高いインデックスiを5つ見つけて、stamp_reward[i,0,:]をCSVに出力
#reward[n]の値が最も低いインデックスiを5つ見つけて、stamp_reward[i,0,:]をCSVに出力

