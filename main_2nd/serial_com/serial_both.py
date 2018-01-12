# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii

import threading

class serial_both:
    def __init__(self, port, baud):
        # シリアル通信の設定(
        self.ser = serial.Serial(port, baud, timeout=1)

    def send_val(self, send_pwm):
        send_str = str(send_pwm)

        self.ser.write(send_str+'deg\0')

    def conbine_high_low(self, str_high,str_low):
        data_high=binascii.b2a_hex(str_high)
        int_high=int(data_high,16)
        high = (int_high << 8)

        data_low=binascii.b2a_hex(str_low)
        int_low=int(data_low,16)
        low = (int_low& 0xFF)

        read_val = (high << 8|low)
        int_val = int(read_val)
        return int_val

    def read_val(self):
        while True:
            serial_data = self.ser.read()
            if serial_data == 'H':
                str_high = self.ser.read()
                str_low = self.ser.read()
                read_val = self.conbine_high_low(str_high,str_low)
                self.ser.flushInput()
                if read_val!= None:
                    print(read_val)
                    #return read_val

if __name__ == '__main__':
    ser_port = "/dev/ttyACM0"
    ser_baud = 19200

    serial_test = serial_both(ser_port,ser_baud)
    th_rcv = threading.Thread(target=serial_test.read_val,name="th_rcv",args=())
    read_ir = th_rcv.start()

    while True:
        print('input send_deg')
        deg =raw_input()
        serial_test.send_val(deg)
        #ser.write(str(deg)+'deg\0')
        if raw_input() == 'exit':
            th_rcv.join()
            print('join')

