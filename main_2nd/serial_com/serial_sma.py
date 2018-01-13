# -*- coding: utf-8 -*-
import serial
import sys

#ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

class Act_sma:
    def __init__(self, port, baud):
        # シリアル通信の設定(
        self.ser = serial.Serial(port, baud, timeout=1)

    def act(self, send_pwm):
        send_str = str(send_pwm)

        self.ser.write(send_str+'deg\0')

if __name__ == '__main__':
    #ser_port = "/dev/ttyACM0"
    ser_baud = 19200

    argvs = sys.argv
    ser_port = argvs[1]

    serial_test = Act_sma(ser_port,ser_baud)

    while True:
        print('input send_deg')
        deg =raw_input()
        serial_test.act(deg)
        #ser.write(str(deg)+'deg\0')

