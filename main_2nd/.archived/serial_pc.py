# -*- coding: utf-8 -*-
import socket
import sys
import threading
import binascii
import numpy as np

class GetSensor:
    def __init__(self, host, port):

        self.num_face = 5

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #IPとPORTを指定してバインドします
        serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）
        print('connecting')

        self.clientsock, self.client_address = serversock.accept() #接続されればデータを格納
        print('connected')

    def check_face(self,face_tmp_list):
        ret = 0
        for t in range(self.num_face):
            if face_tmp_list[t]:
                if face_tmp_list[t] == '':
                    print('face_list',face_tmp_list)
                    print('break')
                    ret = 0
                    return ret

        face_int = map(int,face_tmp_list[0:5])
        for i in range(self.num_face):
            #print('face_tmp_list',face_tmp_list[i])
            if face_int[i]<100 and face_int[i]>=0:
                ret = 1
            else:
                ret = 0
                break
        return ret

    def get_sensor_queue(self, time_window, queue):
        get_face = np.zeros(self.num_face)
        facial = np.zeros((time_window,self.num_face))
        ir_val = np.zeros((time_window,1))
        num_array = 0
        #for t in range(time_window):
        while True:
            rcvmsg = self.clientsock.recv(1024)
            face = rcvmsg.split(",")
            if self.check_face(face) == 1:
                face_int = map(int,face[0:5])
                facial[num_array,:] = np.array(face_int)
                num_array += 1
                print(face_int)
                if num_array > time_window:
                    break

        array = np.hstack((facial,ir_val))
        queue.put(array.T)

    def get_sensor(self, time_window):
        get_face = np.zeros(self.num_face)
        facial = np.zeros((time_window,self.num_face))
        ir_val = np.zeros((time_window,1))
        num_array = 0
        for t in range(time_window):
            rcvmsg = self.clientsock.recv(1024)
            face = rcvmsg.split(",")
            if self.check_face(face) == 1:
                face_int = map(int,face[0:5])
                print(face_int)
                facial[t,:] = np.array(face_int)

        array = np.hstack((facial,ir_val))
        return array.T


    def close():
        clientsock.close()

if __name__ == "__main__" :

    host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
    port = 50000 #クライアントと同じPORTをしてあげます

    get = GetSensor(host,port)
    get.get_sensor(300)
