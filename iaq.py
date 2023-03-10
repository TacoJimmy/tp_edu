import codecs
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import schedule  
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import threading



def Ini_modbus(cport, cbaudrate, csize, cparity,cstop):
    try:
        global master
        master = modbus_rtu.RtuMaster(serial.Serial(port=cport, baudrate=cbaudrate, bytesize=csize, parity=cparity, stopbits=cstop, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
    except:
        pass

def Read_IAQ(id):
    IAQ_Data = master.execute(id, cst.READ_INPUT_REGISTERS, 0, 4)
    IAQ_CO2 = IAQ_Data[0]
    IAQ_VOCt = round(IAQ_Data[1]/230,2)
    IAQ_Temperature = round(IAQ_Data[2]/100,1)
    IAQ_Humidity = round(IAQ_Data[3]/100,1)
    return IAQ_CO2,IAQ_VOCt,IAQ_Temperature,IAQ_Humidity


def Send_Iaq():
    #try:
        Ini_modbus('/dev/ttyUSB0', 9600, 8, "N",1)
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
    #except:
        #pass

schedule.every(1).minutes.do(Send_Iaq) 

if __name__ == '__main__':  
    while True:
        schedule.run_pending()  
        time.sleep(1)
