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
        sma_val = 30
    else:
        sma_val = 0
    return sma_val

if __name__ == '__main__':
    #count = 0

    while True:
        #count+=1

        deg = raw_input()
        deg_int=int(deg,10)
        ser.write(chr(deg_int))
