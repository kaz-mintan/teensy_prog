# -*- coding: utf-8 -*-

from serial_read import *
from serial_sma import *

if __name__ == '__main__':
    ser_port_sma = "/dev/ttyACM0"
    ser_port_ir = "/dev/ttyACM1"
    ser_baud = 19200

    serial_ir = serial_read(ser_port_ir,ser_baud)
    serial_sma = serial_sma(ser_port_sma,ser_baud)
    while True:
        val = serial_ir.read_val()
        print(val)

