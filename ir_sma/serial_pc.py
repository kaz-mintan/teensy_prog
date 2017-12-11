# -*- coding: utf-8 -*-
import serial
import sys
import threading
import binascii

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

#ほんとうかよー
def recvThread():
    serial_data = ser.read()
    print("read",serial_data)
    if serial_data == 'H':
        #ref ir_sma.ino to check the high-low order
        str_high = ser.read()
        data_high=binascii.b2a_hex(str_high)
        int_high=int(data_high,16)
        print('int_high',int_high)
        #print("high",data_high.encode('hex'))
        str_low = ser.read()
        data_low=binascii.b2a_hex(str_low)
        int_low=int(data_low,16)
        print('int_low',int_low)
        #print("low",data_low.encode('hex'))
        #high = ((data_high << 8) & 0xFF)
        high = (int_high << 8)
        #high = bin(bin(data_high >> 8) & 0xFF)
        low = (int_low& 0xFF)
        read_val = (high << 8|low)
        print('read_val',read_val)
        return read_val

def react_formula_thre(ir_value, threshold=50):
    #should be continuous function
    if ir_value > threshold:
        sma_val=60
        print('=========================send!')
    else:
        sma_val=0
        print('===========not send')
    return sma_val

def react_formula(ir_value):
    sma_val=ir_value*2/3
    return sma_val

if __name__ == '__main__':

    #recvT = threading.Thread(target = recvThread)
    #recvT.start()
    read_data=None

    while True:
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
                deg = react_formula(int_val)
                #ser.write(deg)
                #ser.write(str(deg)+"\0")
                #ここでちゃんと遅れてる？
                #終了処理などちゃんとして？

