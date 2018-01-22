# -*- coding: utf-8 -*-
import socket
import numpy as np

class Get_face:
    def __init__(self, host, port):

        self.num_face = 5
        self.num_time = 5
        self.milli = 2

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #IPとPORTを指定してバインドします
        serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）
        print('connecting')

        self.clientsock, self.client_address = serversock.accept() #接続されればデータを格納
        print('connected')

    def check_face(self,face_tmp_list):
        ret = 0
        for t in range(self.num_face+self.num_time):
            if face_tmp_list[t]:
                if face_tmp_list[t].isdigit() == False:
                    ret = 0
                    return ret
                else:
                    ret = 1
        if ret == 1:
            face_int = map(int,face_tmp_list[0:self.num_face+self.num_time])
            for i in range(self.num_face+self.num_time):
                if face_int[i]<100 and face_int[i]>=0:
                    ret = 1
                else:
                    ret = 0
                    break
            return ret

    def check_time(self,face_tmp_list):
        ret = 0
        time_int = map(int,face_tmp_list[self.num_face:self.num_face+self.num_time])
        for i in range(self.num_time):
            if time_int[0]==0 and time_int[4]==0:
                ret = 0
                break
            else:
                ret = 1
        return ret



    def read_face(self):
        get_face = np.zeros(self.num_face)
        tmp_time = np.zeros(self.num_time)
        get_time = np.zeros(self.num_time-self.milli+1)
        rcvmsg = self.clientsock.recv(1024)
        face = rcvmsg.split(",")
        if self.check_face(face) == 1 and self.check_time(face) == 1:
            int_face = map(int,face[0:self.num_face+self.num_time])
            get_face = np.array(int_face[0:self.num_face])
            milli_num = int_face[-2]*10 + int_face[-1]
            get_time = np.hstack((np.array(int_face[self.num_face:self.num_face+self.num_time-self.milli]),np.array([milli_num])))

        return np.array(np.hstack((get_face,get_time)))

    def close():
        clientsock.close()

if __name__ == "__main__" :

    host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
    port = 50000 #クライアントと同じPORTをしてあげます
    type_face = 5
    type_ir = 5

    get = Get_face(host,port)
    while True:
        print(get.read_face())

