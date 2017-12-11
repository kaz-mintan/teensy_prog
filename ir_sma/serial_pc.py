# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

def react_formula(ir_value):
    sma_val=ir_value*2/3
    return sma_val

if __name__ == '__main__':
    host = "192.168.146.128" #お使いのサーバーのホスト名を入れます
    port = 50000 #クライアントと同じPORTをしてあげます

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) #IPとPORTを指定してバインドします
    serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

    print 'Waiting for connections...'
    clientsock, client_address = serversock.accept() #接続されればデータを格納

    while True:
        rcvmsg = clientsock.recv(1024)
        face = rcvmsg.split(",")
        face_int = map(int,face[0:5])
        print face_int
        deg = react_formula(face_int[1])
        ser.write(str(deg)+"\0")

        serial_data = ser.read()
        if serial_data == 'H':
            str_high = ser.read()
            data_high=binascii.b2a_hex(str_high)
            int_high=int(data_high,16)
            str_low = ser.read()
            data_low=binascii.b2a_hex(str_low)
            int_low=int(data_low,16)
            high = (int_high << 8)
            low = (int_low& 0xFF)
            read_val = (high << 8|low)
            int_val = int(read_val)
        #read_data = recvThread()
            if read_val!= None:
                print('main:read_data', int_val, read_val)
                #ここでちゃんと数値が垂れ流されてる？
                #deg = react_formula(int_val)
                #ser.write(deg)
                #ser.write(str(deg)+"\0")
                #ここでちゃんと遅れてる？
                #終了処理などちゃんとして？

    clientsock.close()
