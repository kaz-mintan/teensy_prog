# -*- coding: utf-8 -*-
import serial
import sys
import threading

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

def send_sma():
    # シリアル通信の設定(
    ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)
    shreth = 20

    while True:
        #wait
        if input_ir_val > 0:
            deg = react_formula(input_ir_val,shreth)

        if(deg == "e"):
            ser.close()
            break;

        #sending
        #文字列はいやだ
        ser.write(str(deg)+"\0")


if __name__ == '__main__':
    #main()
    #while True:
        #send_sma()

recvT = threading.Thread(target = recvThread)
recvT.start()

while Ture:
    try:
        kbIn = raw_input()
        if(kbIn == ""):
            recvT.__Thread__stop()
            exit()
        kbIn _ = "/r/n"
        ser.write(kbIn)
    except:
        recvT.__Thread__stop()
        exit()

