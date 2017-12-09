# -*- coding: utf-8 -*-
import serial
import sys
import threading

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

def react_formula(ir_value, shrethold):
    //should be continuous function
    if ir_value > shrethold:
        sma_val=100
    else:
        sma_val=0
    return sma_val

#ほんとうかよー
def recvThread():
    size=3
    readdata = ser.read()
    if readdada == "H":
        #ref ir_sma.ino to check the high-low order
        data_high = ser.read()
        data_low = ser.read()
        high = (data_high >> = 8) & 0xFF
        low = data_low & 0xFF
        read_data = (high << 8|low)
    return read_data

if __name__ == '__main__':

recvT = threading.Thread(target = recvThread)
recvT.start()

while Ture:
    read_data = rectThread()
    print(read_data)
    #ここでちゃんと数値が垂れ流されてる？
    deg = react_formula(read_data)
    ser.write(deg)
    #ここでちゃんと遅れてる？
    #終了処理などちゃんとして？

