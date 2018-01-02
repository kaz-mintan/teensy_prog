# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii

def react_formula(ir_value):
    sma_val=ir_value*1/3
    if ir_value>30:
        sma_val = 30
    else:
        sma_val = 0
    return sma_val

class Serial_com:
    def __init__(self, host, port):

        # シリアル通信の設定(
        ser = serial.serial("/dev/ttyacm0", 9600, timeout=1)

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) #IPとPORTを指定してバインドします
        serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

        clientsock, client_address = serversock.accept() #接続されればデータを格納

    def get_sensor():
        rcvmsg = clientsock.recv(1024)
        face = rcvmsg.split(",")
        face_int = map(int,face[0:5])

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

        return face_int, int_val

    def send_data(data):
        ser.write(chr(data))

    def close():
        clientsock.close()
