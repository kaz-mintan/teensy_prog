# -*- coding: utf-8 -*-

from serial_read import *
from serial_sma import *

import threading

if __name__ == '__main__':
    ser_port_sma = "/dev/ttyACM0"
    ser_port_ir = "/dev/ttyACM1"
    ser_baud = 19200

    serial_ir = serial_read(ser_port_ir,ser_baud)
    serial_sma = serial_sma(ser_port_sma,ser_baud)

    th_rcv = threading.Thread(target=serial_ir.read_val,name="th_rcv",args=())
    th_rcv.start()

    while True:
        deg = raw_input()
        serial_sma.send_val(deg)
        #val = serial_ir.read_val()
        #print(val)

