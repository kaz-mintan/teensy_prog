# -*- coding: utf-8 -*-
import socket
import numpy as np

class Get_face:
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
                if face_tmp_list[t].isdigit() == False:
                #if face_tmp_list[t] == '':
                #if isinstance(face_tmp_list[0],int) == False:
                    #print('face_list',face_tmp_list)
                    #print('break')
                    ret = 0
                    return ret
                else:
                    ret = 1
        if ret == 1:
        #if isinstance(face_tmp_list[0],int) == True:
            face_int = map(int,face_tmp_list[0:5])
            for i in range(self.num_face):
                #print('face_tmp_list',face_tmp_list[i])
                if face_int[i]<100 and face_int[i]>=0:
                    ret = 1
                else:
                    ret = 0
                    break
            return ret

    def read_face(self):
        get_face = np.zeros(self.num_face)
        rcvmsg = self.clientsock.recv(1024)
        face = rcvmsg.split(",")
        if self.check_face(face) == 1:
            int_face = map(int,face[0:5])
            get_face = np.array(int_face)
            #print(get_face)
        return get_face

    def close():
        clientsock.close()

if __name__ == "__main__" :

    host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
    port = 50000 #クライアントと同じPORTをしてあげます

    get = Get_face(host,port)
    while True:
        print(get.read_face())
