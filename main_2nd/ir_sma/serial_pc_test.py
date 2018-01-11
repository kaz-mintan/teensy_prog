# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

def react_formula(ir_value):
    sma_val=ir_value*1/3
    if ir_value>30:
        sma_val = 10
    else:
        sma_val = 0
    return sma_val

if __name__ == '__main__':

    while True:
        deg =raw_input()
        ser.write(deg)
        '''
        serial_data = ser.read()
        if serial_data == 'H':
            str_high = ser.read()
            if str_high != '':
                data_high=binascii.b2a_hex(str_high)
                int_high=int(data_high,16)
            if str_high != '':
                str_low = ser.read()
                data_low=binascii.b2a_hex(str_low)
                int_low=int(data_low,16)
                low = (int_low& 0xFF)
                read_val = (int_high << 8|low)
                int_val = int(read_val)
        #read_data = recvThread()
            if read_val!= None:
                print('main:read_data', int_val)
                #ここでちゃんと数値が垂れ流されてる？
                deg = react_formula(int_val)
                ser.write(chr(deg))
                #ser.write(str(deg)+"\0")
                #ここでちゃんと遅れてる？
                #終了処理などちゃんとして？
                '''
