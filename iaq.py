import codecs
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import schedule  
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import threading

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


def Send_Iaq():
    try:
        
        Iaq = Read_IAQ(1)
        #MQTT_Connect()
        client = mqtt.Client()
        client.on_connect
        client.username_pw_set('WHbLzKWyu35F8fBIV6Hh','WHbLzKWyu35F8fBIV6Hh')
        print(client.connect('thingsboard.cloud', 1883, 60))
    
        payload_iaq = {"CO2":Iaq[0], "VOCt":Iaq[1], "Temperature":Iaq[2],"Humidity":Iaq[3]}
        print(json.dumps(payload_iaq))
        print(client.publish("v1/devices/me/telemetry", json.dumps(payload_iaq)))
        time.sleep(5)
    except:
        pass

schedule.every(1).minutes.do(Send_Iaq) 

if __name__ == '__main__':  
    
    while True:
        schedule.run_pending()  
        time.sleep(1)
