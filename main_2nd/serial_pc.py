# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii
import numpy as np

def react_formula(ir_value):
    sma_val=ir_value*1/3
    if ir_value>30:
        sma_val = 30
    else:
        sma_val = 0
    return sma_val

class GetSensor:
    def __init__(self, host, port):

        # シリアル通信の設定(
        #ser = serial.serial("/dev/ttyacm0", 9600, timeout=1)

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #IPとPORTを指定してバインドします
        serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）
        print('connecting')

        self.clientsock, self.client_address = serversock.accept() #接続されればデータを格納
        print('connected')

    def get_sensor(self, time_window):
        num_face = 5
        get_face = np.zeros(num_face)
        for t in range(time_window):
            rcvmsg = self.clientsock.recv(1024)
            face = rcvmsg.split(",")
            face_int = map(int,face[0:5])
            face_np = np.array(face_int)
            print(t,face_np)

        '''
        serial_data = ser.read()
        if serial_data == 'H':
            str_high = ser.read()
            data_high=binascii.b2a_hex(str_high)
            int_high=int(data_high,16)
            str_low = ser.read()
            data_low=binascii.b2a_hex(str_low)
            int_low=int(data_low,16)
            low = (int_low& 0xFF)
            read_val = (int_high << 8|low)
            int_val = int(read_val)
        '''
        int_val = 0

        #read_data = recvThread()
            #if read_val!= None:
                #ここでちゃんと数値が垂れ流されてる？
                #deg = react_formula(int_val)
                #ser.write(chr(deg))
                #ser.write(str(deg)+"\0")
                #ここでちゃんと遅れてる？
                #終了処理などちゃんとして？

        #return np.hstack((get_face(action[:,episode],argvs[1],argvs[2],t,t_window),get_ir(state[type_face,t-1])))
        return face_int, int_val

    def close():
        clientsock.close()

if __name__ == "__main__" :

    host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
    port = 50000 #クライアントと同じPORTをしてあげます

    get = GetSensor(host,port)
    get.get_sensor(30)
