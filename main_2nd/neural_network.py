import numpy
import math
import random
import matplotlib.pyplot as plt
import itertools
from test_save_txt import *
from datetime import datetime

#from matplotlib import pyplot
type_face = 5

def argmax_ndim(arg_array):
    return numpy.unravel_index(arg_array.argmax(), arg_array.shape)

def nn2q(nn_q):
    changed_q = 25.0*nn_q-12.5
    if changed_q>10:
        changed_q = 10
    elif changed_q<-10:
        changed_q=-10
    return changed_q

def q2nn(q):
    if q>10:
        changed_q=1
    elif q<-10:
        changed_q=0
    else:
        changed_q = 0.04 * q + 0.5
    return changed_q

def rew_q2nn(rew):
    return 0.04*rew

class Neural:

    # constructor
    def __init__(self, n_input, n_hidden, n_output, epsilon, mu, epoch, gamma, alpha):
        self.hidden_weight = numpy.random.random_sample((n_hidden, n_input + 1))
        self.output_weight = numpy.random.random_sample((n_output, n_hidden + 1))
        self.hidden_momentum = numpy.zeros((n_hidden, n_input + 1))
        self.output_momentum = numpy.zeros((n_output, n_hidden + 1))
        self.output_num = n_output

        self.epsilon = epsilon
        self.mu = mu
        self.epoch = epoch

        self.gamma = gamma
        self.alpha = alpha

        self.input_size = n_input
        self.output_size = n_output

    #def train(self, X, T, epsilon, mu, epoch):
    def train(self, X, T):
        self.error = numpy.zeros(self.epoch)
        N = X.shape[0]
        for epo in range(self.epoch):
            #print('nn.py/X[0,:]',X[0,:])
            for i in range(N):
                x = X[i, :]
                t = T[i, :]

                self.__update_weight(x, t, self.epsilon, self.mu)

            self.error[epo] = self.__calc_error(X, T)

        with open('error_log.csv', 'a') as err_handle:
            numpy.savetxt(err_handle,tmp_log(self.error,datetime.now()),fmt="%.5f",delimiter=",",newline="\n")
        with open('output_weight_log.csv', 'a') as out_handle:
            numpy.savetxt(out_handle,self.output_weight,fmt="%.5f",delimiter=",",newline="\n")
        with open('hidden_weight.csv', 'a') as hdn_handle:
            numpy.savetxt(hdn_handle,self.hidden_weight,fmt="%.5f",delimiter=",",newline="\n")

    def predict(self, X):
        N = X.shape[0]
        C = numpy.zeros(N).astype('int')
        Y = numpy.zeros((N, self.output_num))
        for i in range(N):
            x = X[i, :]
            z, y = self.__forward(x)

            Y[i] = y
            C[i] = y.argmax()

        return (C, Y)

    def test_gen_action(self, possible_a, state_mean, episode,random_rate):
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        #possible_q = numpy.zeros((100,100,100))
        possible_q = numpy.zeros((possible_a.shape[0],
            possible_a.shape[0],possible_a.shape[0]))

        ret_random = 0
        ret_action = numpy.array([0,0,0])
        next_q = 0
        dim_num = 3
        val = float(possible_a.shape[0])
        if episode != 0:
            for a,b,c in itertools.product(range(possible_a.shape[0]),repeat=dim_num):
                array = numpy.hstack((possible_a[a],possible_a[b],possible_a[c]))

                p_array[:,0]=numpy.hstack((state_mean[:,episode+1],array))
                C, possible_q[a,b,c]=self.predict(p_array.T)

            if random_rate <= numpy.random.uniform(0, 1):
                ret_random=1#maximize
                action_a,action_b,action_c=argmax_ndim(possible_q)
                #ret_action = numpy.array([action_a/100.0,action_b/100.0,action_c/100.0])
                ret_action = numpy.array([action_a/val,action_b/val,action_c/val])

                next_q=numpy.max(possible_q)
            else:
                ret_random=0 #random
                print('random v')
                action_a = numpy.random.uniform(0,1)
                action_b = numpy.random.uniform(0,1)
                action_c = numpy.random.uniform(0,1)
                ret_action = numpy.array([action_a, action_b, action_c])

                p_array[:,0]=numpy.hstack((state_mean[:,episode+1],ret_action))
                C, next_q=self.predict(p_array.T)

        filename ='{0}{1}{2}'.format('q_possible/q_possible_',episode,'.npy')
        with open(filename, 'a') as qa_handle:
            numpy.save(qa_handle,possible_q)

        with open('q_possible/q_possible_a.csv', 'a') as qa_handle:
            numpy.savetxt(qa_handle,tmp_log(numpy.hstack((np.array([episode]),possible_q[:,int(ret_action[1]*val),int(ret_action[2]*val)])),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")
        with open('q_possible/q_possible_b.csv', 'a') as qb_handle:
            numpy.savetxt(qb_handle,tmp_log(numpy.hstack((np.array([episode]),possible_q[int(ret_action[0]*val),:,int(ret_action[2]*val)])),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")
        with open('q_possible/q_possible_c.csv', 'a') as qc_handle:
            numpy.savetxt(qc_handle,tmp_log(numpy.hstack((np.array([episode]),possible_q[int(ret_action[0]*val),int(ret_action[1]*val),:])),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")

        with open('action_row.csv', 'a') as act_handle:
            numpy.savetxt(act_handle,tmp_log(numpy.hstack((np.array([episode]),ret_action)),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")

        with open('p_array_gen.csv', 'a') as act_handle:
            numpy.savetxt(act_handle,tmp_log(numpy.hstack((np.array([episode]),p_array.T)),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")



        return ret_random, ret_action, next_q

    def reculc_gen_action(self, possible_a, state_mean, episode,random_rate):
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        #possible_q = numpy.zeros((100,100,100))
        possible_q = numpy.zeros((possible_a.shape[0],
            possible_a.shape[0],possible_a.shape[0]))

        ret_random = 0
        ret_action = numpy.array([0,0,0])
        next_q = 0
        small_q = 0
        dim_num = 3
        val = float(possible_a.shape[0])
        if episode != 0:
            for a,b,c in itertools.product(range(possible_a.shape[0]),repeat=dim_num):
                array = numpy.hstack((possible_a[a],possible_a[b],possible_a[c]))

                p_array[:,0]=numpy.hstack((state_mean[:,episode+1],array))
                C, possible_q[a,b,c]=self.predict(p_array.T)

            #if random_rate <= numpy.random.uniform(0, 1):
            ret_random=1#maximize
            action_a,action_b,action_c=argmax_ndim(possible_q)
            #ret_action = numpy.array([action_a/100.0,action_b/100.0,action_c/100.0])
            ret_action = numpy.array([action_a/val,action_b/val,action_c/val])

            next_q=numpy.max(possible_q)
            small_q=numpy.min(possible_q)

            with open('p_array_learn.csv', 'a') as act_handle:
                numpy.savetxt(act_handle,tmp_log(p_array[0,:],datetime.now()),fmt="%.5f",delimiter=",",newline="\n")

        return ret_random, ret_action, next_q, small_q

    def reproduct_test(self, state_mean, action, q_teacher, noize_rate, episode_num):
        print('q_teacher',q_teacher)
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        q_array= numpy.zeros((self.output_size,1)) #to stock predicted argument
        p_array[:,0]=numpy.hstack((state_mean[:,episode_num],action[:,episode_num]))
        for i in range(7):
            noize_array = p_array
            val = p_array[i,0]
            noize_array[i,0]+=0.01*val

            C,predict_answer = self.predict(noize_array.T)
            print(i,p_array.T,noize_array.T)
            print("pre,ans",predict_answer, q2nn(q_teacher[:,episode_num]))
            ans =q2nn(q_teacher[:,episode_num])
            print('check_noize',noize_array[:,0])
            print('check_p-array',p_array[:,0])
            print('check_predict',predict_answer[:,0])
            print('check_ans',ans)

            with open('reproduct_test.csv', 'a') as act_reprod:
                numpy.savetxt(act_reprod,tmp_log(numpy.hstack((noize_array[:,0],p_array[:,0],predict_answer[:,0],ans)),datetime.now()),fmt="%.5f",delimiter=",",newline="\n")


    def update(self, state_mean, action, episode, q_teacher, reward, next_q):
        #reward, next_q, gamma, alpha):
        # set input_array to predict
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        q_array= numpy.zeros((self.output_size,1)) #to stock predicted argument
        p_array[:,0]=numpy.hstack((state_mean[:,episode],action[:,episode]))

        # calculate present_q based on present state value
        C, present_q = self.predict(p_array.T)#nn_val

        #if alpha*((reward[episode+1])+gamma*nn2q(next_q)-nn2q(present_q[0,0])) >0:
        q_teacher[:,episode] = nn2q(present_q[0,0]) + \
                self.alpha*((reward[episode+1])+self.gamma*nn2q(next_q)-nn2q(present_q[0,0]))
        print('nn/reward',reward[episode+1])

        q_array[:,0]=q2nn(q_teacher[:,episode])

        return q_teacher

    #def predict_update(self, state_mean, state_predict,num_action, num_face, action, episode, p_teacher,
    def predict_update(self, state_mean, state_predict, action, episode, p_teacher,
            reward, next_q):
            #reward, next_q, gamma, alpha):

        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        q_array= numpy.zeros((self.output_size,1)) #to stock predicted argument

        p_array[:,0]=numpy.hstack((state_mean[:,episode+1],
            action[:,episode+1]))
        C, face_predict =self.predict(p_array.T)
        state_predict[0,:type_face] = face_predict

        p_teacher[:,episode] = state_mean[:type_face,episode]
        q_array[:,0]=p_teacher[:,episode]

        self.train(p_array.T,q_array)
        return state_predict, p_teacher

# private method
    def __sigmoid(self, arr):
        return numpy.vectorize(lambda x: 1.0 / (1.0 + math.exp(-x)))(arr)

    def __forward(self, x):
        # z: output in hidden layer, y: output in output layer
        z = self.__sigmoid(self.hidden_weight.dot(numpy.r_[numpy.array([1]), x]))
        y = self.__sigmoid(self.output_weight.dot(numpy.r_[numpy.array([1]), z]))

        return (z, y)

    def __update_weight(self, x, t, epsilon, mu):
        z, y = self.__forward(x)

        # update output_weight
        output_delta = (y - t) * y * (1.0 - y)
        _output_weight = self.output_weight
        self.output_weight -= epsilon * output_delta.reshape((-1, 1)) * numpy.r_[numpy.array([1]), z] - mu * self.output_momentum
        self.output_momentum = self.output_weight - _output_weight

        # update hidden_weight
        hidden_delta = (self.output_weight[:, 1:].T.dot(output_delta)) * z * (1.0 - z)
        _hidden_weight = self.hidden_weight
        self.hidden_weight -= epsilon * hidden_delta.reshape((-1, 1)) * numpy.r_[numpy.array([1]), x]
        self.hidden_momentum = self.hidden_weight - _hidden_weight

    def __calc_error(self, X, T):
        N = X.shape[0]
        err = 0.0
        for i in range(N):
            x = X[i, :]
            t = T[i, :]

            z, y = self.__forward(x)
            err += (y - t).dot((y - t).reshape((-1, 1))) / 2.0

        return err


if __name__ == '__main__':

    print('1')

    X = numpy.array([[-2, 0.5,2], [0, 0.1,3], [1, 0,0.2], [1, 1,0.4]])
    T = numpy.array([[1, 0.2], [0.3, 1], [0.5, 1], [1, 0]])
    N = X.shape[0] # number of data

    input_size = X.shape[1]
    hidden_size = X.shape[1]
    output_size = T.shape[1]

    epsilon = 0.1
    mu = 0.9
    epoch = 10000

    print('2')
    nn = Neural(input_size, hidden_size, output_size,epsilon, mu, epoch, 1,1)
    print('3')
    #nn.train(X, T, epsilon, mu, epoch)
    nn.train(X, T)
    #nn.error_graph()

    print('4')
    #print('print',nn.predict(X,T))
    C, Y = nn.predict(X)

    X2 = numpy.array([[-2.1, 0.5,2], [0, 0.1,2.5], [1, -0.1,0.2], [-0.1, 1,0.4]])
    print(nn.predict(X2))


    for i in range(N):
        x = X[i, :]
        y = Y[i, :]
        c = C[i]

        print x
        print y
        print c
