# -*- coding: utf-8 -*-
import serial
import sys
import time
import numpy as np

#ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

class Act_sma:
    def __init__(self, port, baud):
        # シリアル通信の設定(
        self.ser = serial.Serial(port, baud, timeout=1)

    def act(self, send_pwm):
        send_str = str(send_pwm)

        #self.ser.write(send_str+'deg\0')
        self.ser.write(send_str+'\0')

    #def send_para(self, pwm_input,keep,delay_time):
    def send_para(self, action):
        pwm_input = action[0]
        keep_val = int(float(action[1])*10)
        delay_val = int(float(action[2])*10)
        array_num = action[3]
        print(pwm_input,keep_val,delay_val,array_num)
        self.act(pwm_input)
        self.act(keep_val)
        self.act(delay_val)
        self.act(array_num)

if __name__ == '__main__':
    #ser_port = "/dev/ttyACM0"
    ser_baud = 19200

    argvs = sys.argv
    ser_port = argvs[1]

    serial_test = Act_sma(ser_port,ser_baud)

    while True:
        print('input pwm')
        pwm = raw_input()
        print('input keep')
        keep = raw_input()
        print('input delay')
        delay = raw_input()
        print('input aarray_num')
        array_num = raw_input()


        serial_test.send_para(np.array([pwm,keep,delay,array_num]))
        #serial_test.act(deg)
        #ser.write(str(deg)+'deg\0')

