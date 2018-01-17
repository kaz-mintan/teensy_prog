# -*- coding: utf-8 -*-
from socket_com import socket_face
from serial_com import serial_read5
import numpy as np

#def get_state(ser_port, ser_baud, soc_host, soc_port):
class Get_state:
    def __init__(self,ser_port, ser_baud, soc_host, soc_port):
        self.ir_sensor = serial_read5.Serial_read(ser_port,ser_baud)
        self.face_sensor = socket_face.Get_face(soc_host,soc_port)

    def ret_state(self):
        ir_val = self.ir_sensor.read_val()
        face_sensor = self.face_sensor.read_face()

        np_ir = np.array(ir_val)
        np_face = np.array(face_sensor)

        #state_array = np.hstack(face_sensor,ir_val)
        state_array = np.hstack((np_face,np_ir))
        return state_array

def extract_state(state_array):
    type_face = 5
    type_ir = 5
    num_timestamp = 4

    return np.hstack((state_array[:type_face],state_array[type_face+num_timestamp:]))

def extract_time(state_array):
    type_face = 5
    type_ir = 5
    num_timestamp = 4

    return state_array[type_face:type_face+num_timestamp]

if __name__ == "__main__" :
    type_face = 5
    type_ir = 5
    num_timestamp = 4

    state = np.zeros((type_face+type_ir+num_timestamp,1))
    state[:,0]=np.array([1,1,1,1,1,3,3,3,3,7,7,7,7,7])
    print(state[:,0])
    print(extract_state(state[:,0]))
    print(extract_time(state[:,0]))


    ser_port = "/dev/ttyACM1"
    ser_baud = 19200

    soc_host = "192.168.146.128" #お使いのサーバーのホスト名
    soc_port = 50000 #クライアントと同じPORT

    state = Get_state(ser_port, ser_baud, soc_host, soc_port)
    while True:
        val = state.ret_state()
        print('stacked',val)

