import codecs
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
 
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import time
import struct


def int16_pair_to_float(num1, num2):
    combined_num = (num1 << 16) | num2
    packed_num = struct.pack('i', combined_num)
    float_num = struct.unpack('f', packed_num)[0]
    return float_num

def Read_IAQ(id):
    global master
    master = modbus_tcp.TcpMaster(host="192.168.1.110")
    master.set_timeout(5.0)
    IAQ_Data = master.execute(id, cst.READ_INPUT_REGISTERS, 0, 8)
    CO2 = int16_pair_to_float(IAQ_Data[1], IAQ_Data[0])
    VOC = int16_pair_to_float(IAQ_Data[3], IAQ_Data[2])
    temp = int16_pair_to_float(IAQ_Data[5], IAQ_Data[4])/100
    humi = int16_pair_to_float(IAQ_Data[7], IAQ_Data[6])/100

    time.sleep(1)
    
    return CO2,VOC,temp,humi

print (Read_IAQ(1))