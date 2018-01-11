# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

def react_formula(ir_value):
    sma_val=ir_value*2/3
    return sma_val

if __name__ == '__main__':

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
            ser.flushInput()
        #read_data = recvThread()
            if read_val!= None:
                print(read_val)
                #ここでちゃんと数値が垂れ流されてる？
                #deg = react_formula(int_val)
                #ser.write(deg)
                #ser.write(str(deg)+"\0")
                #ここでちゃんと遅れてる？
                #終了処理などちゃんとして？

