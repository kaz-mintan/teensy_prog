import numpy
import math
import random
#from matplotlib import pyplot
select_episode = 10
type_face = 5

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
    def __init__(self, n_input, n_hidden, n_output, epsilon, mu, epoch):
        self.hidden_weight = numpy.random.random_sample((n_hidden, n_input + 1))
        self.output_weight = numpy.random.random_sample((n_output, n_hidden + 1))
        self.hidden_momentum = numpy.zeros((n_hidden, n_input + 1))
        self.output_momentum = numpy.zeros((n_output, n_hidden + 1))
        self.output_num = n_output

        self.epsilon = epsilon
        self.mu = mu
        self.epoch = epoch

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

    def gen_action(self, possible_a, num_action, num_face, state_mean, episode,random_rate,action,reward,alpha,q_table):
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        q_array= numpy.zeros((self.output_size,1)) #to stock predicted argument
        possible_q = numpy.zeros(100)
        memo_q=numpy.zeros((1,100))

        '''
        if episode == 0:
            p_array[:,0]=numpy.hstack((state_mean[:,episode],action[0,episode]))
            q_array[:,0] = alpha*q2nn(reward[episode+1])
            self.train(p_array.T,q_array.T)

            selected_action = numpy.random.uniform(0,1)
            random=0
            #next_q = 0#at this point
            p_array[:,0]=numpy.hstack((state_mean[:,episode+1],selected_action))
            C, next_q = self.predict(p_array.T)#at this point

        else:
        '''
        if episode<300:
            selected_action=numpy.random.uniform(0,1)#TODO not enough
            random=0 #random

        elif episode>=300:
            for i in range(100):
                p_array[:,0]=numpy.hstack((state_mean[:,episode+1],possible_a[i]))
                C, possible_q[i]=self.predict(p_array.T)

            if random_rate <= numpy.random.uniform(0, 1):
                random=1#maximize
                selected_action=(numpy.argmax(possible_q))/100.0
            else:
                selected_action=numpy.random.uniform(0,1)#TODO not enough
                random=0 #random

            next_q=numpy.max(possible_q)

        return random, selected_action, next_q

    def update(self, state_mean, num_action, num_face, action, episode, q_teacher,
            reward, next_q, select_episode, gamma, alpha):

        # set input_array to predict
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        q_array= numpy.zeros((self.output_size,1)) #to stock predicted argument
        p_array[:,0]=numpy.hstack((state_mean[:,episode],action[:,episode]))

        # calculate present_q based on present state value
        C, present_q = self.predict(p_array.T)#nn_val

        q_teacher[:,episode] = nn2q(present_q[0,0]) + \
                alpha*((reward[episode+1])+gamma*nn2q(next_q)-nn2q(present_q[0,0]))
        print('nn/present_q etc',nn2q(present_q[0,0]),gamma*nn2q(next_q))

        q_array[:,0]=q2nn(q_teacher[:,episode])
        #print('checkl',q_array[:,0],q_teacher[:,episode],q2nn(q_teacher[:,episode]))

        memo=numpy.zeros((1,2))
        memo[0,0]=nn2q(present_q[0,0])
        memo[0,1]=nn2q(next_q)
        with open('next_q.csv', 'a') as f_handle:
            numpy.savetxt(f_handle,memo,fmt="%.5f",delimiter=",",newline="\n")
 
        self.train(p_array.T,q_array)

        ##for debug
        c, ans = self.predict(p_array.T)
        #print('nncheck',q_array[:,0],ans)

        ##for debug
        possible_a = numpy.linspace(0,1,100)
        p_array= numpy.zeros((self.input_size,1)) #to stock predicted argument
        possible_q = numpy.zeros(100)
        memo_q=numpy.zeros((1,100))

        for i in range(100):
            p_array[:,0]=numpy.hstack((state_mean[:,episode+1],possible_a[i]))
            C, possible_q[i]=self.predict(p_array.T)

        memo_q[0,:]=possible_q
        with open('q_func_curve_after_learning.csv', 'a') as f_handle:
            numpy.savetxt(f_handle,memo_q,fmt="%.5f",delimiter=",",newline="\n")

        return q_teacher

    def predict_update(self, state_mean, state_predict,num_action, num_face, action, episode, p_teacher,
            reward, next_q, select_episode, gamma, alpha):

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

    for i in numpy.linspace(-20,20,40):
        print(i,q2nn(i))

    raw_input()

    print('1')
    X = numpy.array([[2, 0.5,2], [0, 0.1,3], [1, 0,0.2], [1, 1,0.4]])
    T = numpy.array([[1, 2], [3, 1], [0.5, 1], [1, 0]])
    #X = numpy.zeros((4,3))
    #T = numpy.zeros((4,2))
    #Y = numpy.array([[1], [0], [0.2], [0.4]])
    N = X.shape[0] # number of data

    input_size = X.shape[1]
    hidden_size = X.shape[1]
    output_size = T.shape[1]

    epsilon = 0.1
    mu = 0.9
    epoch = 10000

    print('2')
    nn = Neural(input_size, hidden_size, output_size)
    print('3')
    nn.train(X, T, epsilon, mu, epoch)
    #nn.error_graph()

    print('4')
    #print('print',nn.predict(X,T))
    C, Y = nn.predict(X)
    print(C,Y)

    for i in range(N):
        x = X[i, :]
        y = Y[i, :]
        c = C[i]

        print x
        print y
        print c
