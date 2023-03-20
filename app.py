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
import struct
import IAQ_Sensor
import power_meter


def Send_IAQValue():
    try:
        IAQ_Value = IAQ_Sensor.Read_IAQ(1)
        #MQTT_Connect()
        clientsub = mqtt.Client()
        clientsub.on_connect
        clientsub.username_pw_set('d0L7daAjF3J89ebJZfEk','')
        print(clientsub.connect('thingsboard.cloud', 1883, 60))
    
        payload_iaq = {"CO2":IAQ_Value[0],
                       "PM25":IAQ_Value[1],
                       "PM10":IAQ_Value[2],
                       "CO":IAQ_Value[3],
                       "HCHO":IAQ_Value[4],
                       "ammonia":IAQ_Value[5],
                       "O2":IAQ_Value[6],
                       "TVOC":IAQ_Value[7],
                       "Temperature":IAQ_Value[8],
                       "Humidity":IAQ_Value[9],
                       }
        print(json.dumps(payload_iaq))
        clientsub.publish("v1/devices/me/telemetry", json.dumps(payload_iaq))
        time.sleep(5)
        return IAQ_Value
    except:
        print ("error")


def Send_MainPower():
    try:
        PowerFrq_Value = power_meter.Read_PowerFreq()
        PowerVoltage = power_meter.Read_MainPowerVoltage()
        PowerCurrnet = power_meter.Read_MainPowerCurrnet()
        PowerkW = power_meter.Read_MainPowerkW()
        PowerkVAR = power_meter.Read_MainPowerkVAR()
        PowerkVAS = power_meter.Read_MainPowerkVAS()
        #MQTT_Connect()
        client = mqtt.Client()
        client.on_connect
        client.username_pw_set('KMS1AXvpxzHiuEHx3G6t','')
        print(client.connect('thingsboard.cloud', 1883, 60))
    
        payload_iaq = {"PowerFrq":PowerFrq_Value,
                       "PowerV1":PowerVoltage[0],
                       "PowerV2":PowerVoltage[1],
                       "PowerV3":PowerVoltage[2],
                       "PowerVavg":PowerVoltage[3],
                       "PowerI1":PowerCurrnet[0],
                       "PowerI2":PowerCurrnet[1],
                       "PowerI3":PowerCurrnet[2],
                       "PowerIavg":PowerCurrnet[3],
                       "PowerkW1":PowerkW[0],
                       "PowerkW2":PowerkW[1],
                       "PowerkW3":PowerkW[2],
                       "PowerkWavg":PowerkW[3],
                       "PowerkVAR1":PowerkVAR[0],
                       "PowerkVAR2":PowerkVAR[1],
                       "PowerkVAR3":PowerkVAR[2],
                       "PowerkVARavg":PowerkVAR[3],
                       "PowerkVAS1":PowerkVAS[0],
                       "PowerkVAS2":PowerkVAS[1],
                       "PowerkVAS3":PowerkVAS[2],
                       "PowerkVASavg":PowerkVAS[3]
                       }
        print(json.dumps(payload_iaq))
        print(client.publish("v1/devices/me/telemetry", json.dumps(payload_iaq)))
        time.sleep(5)
    except:
        power_meter.create_modbus_connection()
        print ("error")

def Send_SubPower():
    try:
        for i in range(4):
            PowerCurrnet = power_meter.Read_SubPowerCurrnet(i)
            PowerkW = power_meter.Read_SubPowerkW(i)
            PowerkVAR = power_meter.Read_SubPowerkVAR(i)
            PowerkVAS = power_meter.Read_SubPowerkVAS(i)
            #MQTT_Connect()
            clientsub = mqtt.Client()
            clientsub.on_connect
            clientsub.username_pw_set('q62EdLRp3iUrFHDFeg4i','')
            print(clientsub.connect('thingsboard.cloud', 1883, 60))
    
            payload_iaq = {"SubPowerI1"+str(i):PowerCurrnet[0],
                       "SubPowerI2"+str(i):PowerCurrnet[1],
                       "SubPowerI3"+str(i):PowerCurrnet[2],
                       "SubPowerIavg"+str(i):PowerCurrnet[3],
                       "SubPowerkW1"+str(i):PowerkW[0],
                       "SubPowerkW2"+str(i):PowerkW[1],
                       "SubPowerkW3"+str(i):PowerkW[2],
                       "SubPowerkWavg"+str(i):PowerkW[3],
                       "SubPowerkVAR1"+str(i):PowerkVAR[0],
                       "SubPowerkVAR2"+str(i):PowerkVAR[1],
                       "SubPowerkVAR3"+str(i):PowerkVAR[2],
                       "SubPowerkVARavg"+str(i):PowerkVAR[3],
                       "SubPowerkVAS1"+str(i):PowerkVAS[0],
                       "SubPowerkVAS2"+str(i):PowerkVAS[1],
                       "SubPowerkVAS3"+str(i):PowerkVAS[2],
                       "SubPowerkVASavg"+str(i):PowerkVAS[3]
                       }
            print(json.dumps(payload_iaq))
            print(clientsub.publish("v1/devices/me/telemetry", json.dumps(payload_iaq)))
            time.sleep(5)
    except:
        power_meter.create_modbus_connection()
        print ("error")

#schedule.every(1).minutes.do(Send_IAQValue)
schedule.every(1).minutes.do(Send_MainPower)
schedule.every(1).minutes.do(Send_SubPower)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)

