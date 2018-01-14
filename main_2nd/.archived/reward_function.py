# coding:utf-8

def facial_reward(facial):
    reward_weight = np.array([0,100,40,-50,-50])
    if(facial.size==reward_weight.size):
        reward = np.dot(facial, reward_weight)
    return reward

