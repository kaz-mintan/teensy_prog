# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

def save_file(num_episodes,action,target_type,target_direct,mode):

    file_name = 'action_%s_%s_%s.png' % (target_type,target_direct,mode)
    plt.legend() # 凡例を表示

    plt.title(file_name)
    plt.xlabel("num of episode")
    plt.ylabel("action value")
    plt.plot(np.linspace(0,num_episodes,num_episodes),action[0,:],marker="o",linestyle="dashed")
    plt.savefig(file_name)
