# coding:utf-8
import numpy as np
import math


def linear_state(state):
    state_feature = np.mean(state, axis=1)
    return state_feature

