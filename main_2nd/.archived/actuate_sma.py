# -*- coding: utf-8 -*-
import serial
import time

class Serial_com: 

    def __init__(self, port, baud):
        ser = serial.Serial(port, baud, timeout=1)

    def action(self, pwm):
        ser.write(str(pwm)+"\0")
        print('pwm',pwm)
        print('serius hage!')
        #time.sleep(pwm*10)
        #move_flg =0
        #return move_flg

def main():

    # シリアル通信の設定(
    ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)
    while True:
        # 入力待機（回転させたい角度を入力）
        deg = raw_input()
        # eが入力されたら終了
        if(deg == "e"):
            ser.close()
            break;
        # 回転角と終端文字を送信
        ser.write(str(deg)+"\0")

def react_formula(ir_value, shreth):
    if ir_value > shreth:
        sma_val=100
    else:
        sma_val=0
    return sma_val

def send_sma():
    # シリアル通信の設定(
    ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)
    shreth = 20

    while True:
        #wait
        if input_ir_val > 0:
            deg = react_formula(input_ir_val,shreth)

if __name__ == '__main__':
    #send_sma()
    port = "/dev/ttyACM0"
    baud = 19200

    ser = serial.Serial(port, baud, timeout=1)
    print('input')
    pwm = raw_input()
    ser.write(pwm+"\0")
 
    #main()
    sma = Serial_com(port,baud)

    while 1:
        deg = raw_input()
        sma.action(deg)

