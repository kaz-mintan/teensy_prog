# coding:utf-8
import numpy as np

def save_stamp(stamp_reward, time_reward, state_reward,episode):
    print('state_reward',state_reward.shape)
    print('time_reward',time_reward.shape)
    stamp_reward[episode,0,:]=\
            np.hstack((np.array([np.argmax(state_reward[1,2:])+2]),\
            time_reward[:,np.argmax(state_reward[1,2:])+2]))

    stamp_reward[episode,1,:]=\
            np.hstack((np.array([np.argmin(state_reward[1,2:])+2]),\
            time_reward[:,np.argmin(state_reward[1,2:])+2]))
    return stamp_reward

if __name__ == '__main__':
    type_face = 5
    type_ir = 5
    num_timestamp = 4
    num_episodes = 6

    state_reward = np.zeros((type_face+type_ir,num_episodes))
    time_reward = np.zeros((num_timestamp,num_episodes))
    stamp_reward = np.zeros((num_episodes,2,num_timestamp+1))

    state_reward=np.random.randint(low=0,high=100,size=state_reward.shape)
    time_reward=np.random.randint(low=0,high=100,size=time_reward.shape)
    print('main/state_reward',state_reward)
    print('main/time_reward',time_reward)
    episode = 0

    stamp_reward = save_stamp(stamp_reward, time_reward, state_reward, episode)
    print(save_stamp(stamp_reward, time_reward, state_reward, episode))

    reward[np.argsort(reward)[-i]]
    stamp_reward[np.argsort(reward)[-i],0,:]
