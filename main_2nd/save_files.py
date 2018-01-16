# coding:utf-8

import numpy as np

from datetime import datetime

#datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#now = datetime.datetime.now()
#print('test_{0:%Y%m%d}'.format(now)) #test_20170910

class Save_csv:
    def __init__(self, now_time):
        self.state_name = 'state_%Y%m%d%H%M%S.csv'.format(now_time)
        self.action_name = 'action_%Y%m%d%H%M%S.csv'.format(now_time)
        self.face_name = 'face_%Y%m%d%H%M%S.csv'.format(now_time)
        self.random_name = 'random_%Y%m%d%H%M%S.csv'.format(now_time)

    def stack_array_date(self, array, now):
        time_array = np.array([now.hour,now.minute,now.second,now.microsecond])
        stucked_array = np.hstack((array,time_array))
        return stucked_array

    #ランダムは配列としてうまく保存できるだろうか？
    def save_state(self,state,now):
        state_stack=self.stack_array_date(state, now)
        with open(self.state_name, 'a') as f_state:
            np.savetxt(f_state,state,fmt="%.5f",delimiter=",",newline="\n")

    def save_action(self,action,now):
        action_stack=self.stack_array_date(action, now)
        with open(self.action_name, 'a') as f_action:
            np.savetxt(f_action,action,fmt="%.5f",delimiter=",",newline="\n")

    def save_face(self, face,now):
        face_stack=self.stack_array_date(face,now)
        with open(self.face_name, 'a') as f_face:
            np.savetxt(f_face,face,fmt="%.5f",delimiter=",",newline="\n")

    def save_random(self, random,now):
        random_stack=self.stack_array_date(random,now)
        with open(self.random_name, 'a') as f_random:
            np.savetxt(f_random,random,fmt="%.5f",delimiter=",",newline="\n")
    def save_all(self,state,action,face,random,now):
        self.save_state(state,now)
        self.save_action(action,now)
        self.save_face(face,now)
        self.save_random(random,now)
   #np.savetxt(f_handle,memo_q,fmt="%.5f",delimiter=",",newline="\n")
