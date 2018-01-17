# coding:utf-8
import numpy as np

def save_stamp(stamp_reward, time_reward, state_reward,episode):
    stamp_reward[episode,0,:]=time_reward[:,np.argmax(state_reward[1,:])]
    stamp_reward[episode,1,:]=time_reward[:,np.argmin(state_reward[1,:])]
    return stamp_reward

if __name__ == '__main__':
    type_face = 5
    type_ir = 5
    num_timestamp = 4
    num_episodes = 4

    state_reward = np.zeros((type_face+type_ir,5))
    time_reward = np.zeros((num_timestamp,5))
    stamp_reward = np.zeros((num_episodes,2,num_timestamp))

    state_reward=np.random.randint(low=0,high=100,size=state_reward.shape)
    time_reward=np.random.randint(low=0,high=100,size=time_reward.shape)
    print('main/state_reward',state_reward)
    print('main/time_reward',time_reward)
    for episode in range(4):
        stamp_reward = save_stamp(stamp_reward, time_reward, state_reward, episode)

    print(stamp_reward)
