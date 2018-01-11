# -*- coding: utf-8 -*-
import serial

# シリアル通信の設定(
ser = serial.Serial("/dev/ttyACM0", 19200, timeout=1)

while True:
    deg =raw_input()
    ser.write(str(deg)+'deg\0')
