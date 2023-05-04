'''
Created on 2023/4/8

@author: infilink_Jimmy
'''

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
import IAQ_Sensor
import random
import power_meter


# make check
TVOC_Limit_Flog = 0
CO2_Limit_Flog = 0
CO2_Limit = 1000
TVOC_Limit = 100

def Send_MainPower():
    try:
        PowerFrq_Value = power_meter.Read_PowerFreq()
        PowerVoltage = power_meter.Read_MainPowerVoltage()
        PowerCurrnet = power_meter.Read_MainPowerCurrnet()
        PowerkW = power_meter.Read_MainPowerkW()
        PowerkVAR = power_meter.Read_MainPowerkVAR()
        PowerkVAS = power_meter.Read_MainPowerkVAS()
        PowerkWh = power_meter.Read_MainPowerComsumption()
        PowerDM = power_meter.Read_MainPowerDM()
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
                       "PowerkVASavg":PowerkVAS[3],
                       "PowerkWh":PowerkWh[0],
                       "PowerDM":PowerDM[0]
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

# IAQ over limit send linebot
def Send_LineBot(IAQ_Cond,IAQ_value):
    try:
        client = mqtt.Client()
        client.on_connect
        client.username_pw_set('4zhS0DhTPpLMnatCAlr8','XXX')
        client.connect('thingsboard.cloud', 1883, 60)
        if IAQ_Cond =="CO2":
            payload_iaq = {"to":"U0e6cd17312489c36553152020d7af0b9","messages":[{"type":"text","text":"CO2濃度超過設定值，目前濃度為："+str(IAQ_value)+"ppm"}]}
        #payload_iaq = {"temperature":24}
        
        if IAQ_Cond == "TVOC":
            payload_iaq = {"to":"U0e6cd17312489c36553152020d7af0b9","messages":[{"type":"text","text":"TVOC濃度超過設定值，目前濃度為:"+str(IAQ_value)+"ppm"}]}
        
        print(client.publish("v1/devices/me/telemetry", json.dumps(payload_iaq)))
        time.sleep(5)
    except:
        pass

def Send_Iaq():
    global CO2_Limit_Flog
    global TVOC_Limit_Flog
    try:
        #gate iaq data
        IAQ_Data = IAQ_Sensor.Read_IAQ(1)
        #IAQ_Data = [500,60,25,70]
        if IAQ_Data != "None":
            CO2 = IAQ_Data[0]
            TVOC = IAQ_Data[1]
            Temperature = IAQ_Data[2]
            Humidity = IAQ_Data[3]
            
            client = mqtt.Client()
            client.on_connect
            client.username_pw_set('d0L7daAjF3J89ebJZfEk','XXX')
            client.connect('thingsboard.cloud', 1883, 60)
            payload_iaq = {"CO2":CO2,"TVOC":TVOC,"Temperature":Temperature,"Humidity":Humidity}
            print(client.publish("v1/devices/me/telemetry", json.dumps(payload_iaq)))
            time.sleep(5)
            
        else:
            print("Can't read IAQ data")
    except:
        pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+',1)
    time.sleep(3)

def on_message(client, userdata, msg):
    global CO2_Limit
    global TVOC_Limit
    try: 
        data_topic = msg.topic
        data_payload = json.loads(msg.payload.decode())
        time.sleep(.5)
        #print (data_topic)
        print (data_payload)
    
        if data_payload['method'] == "CO2":
            IAQ_CO2Limit = int(data_payload['params'])
            if IAQ_CO2Limit >= 400 & IAQ_CO2Limit <= 2000:
                IAQ_Sensor.write_CO2_Limit(IAQ_CO2Limit)
                time.sleep(1)
                payload_iaq = {"CO2_Limit":IAQ_CO2Limit}
                client.publish("v1/devices/me/attributes", json.dumps(payload_iaq))
                time.sleep(5)
                CO2_Limit = IAQ_CO2Limit
                
        if data_payload['method'] == "TVOC":
            IAQ_TVOCLimit = int(data_payload['params'])
            if IAQ_TVOCLimit >= 50 & IAQ_TVOCLimit <= 200:
                IAQ_Sensor.write_TVOC_Limit(IAQ_TVOCLimit)
                time.sleep(1)
                payload_iaq = {"TVOC_Limit":IAQ_TVOCLimit}
                client.publish("v1/devices/me/attributes", json.dumps(payload_iaq))
                time.sleep(5)
                TVOC_Limit = IAQ_TVOCLimit
    except:
        pass
    
    #client.publish(signal_fb,json.dumps(fb_payload)) # send response

def ipc_subscribe():
    try:
        meter_token = "d0L7daAjF3J89ebJZfEk"
        meter_pass = ''
        url = 'thingsboard.cloud'

        client_s = mqtt.Client()
        client_s.on_connect = on_connect
        time.sleep(.5)
        client_s.on_message = on_message
        time.sleep(.5)
        client_s.username_pw_set(meter_token, meter_pass)
        client_s.connect(url, 1883, 60)
        client_s.loop_forever()
    except:
        print ("Can't connect network")

def check_Iaq():
    global CO2_Limit_Flog
    global TVOC_Limit_Flog
    global CO2_Limit
    global TVOC_Limit
    try:
        #gate iaq data
        IAQ_Data = IAQ_Sensor.Read_IAQ(1)
        #IAQ_Data = [500,60,25,70]
        if IAQ_Data != "None":
            CO2 = IAQ_Data[0]
            TVOC = IAQ_Data[1]
            Temperature = IAQ_Data[2]
            Humidity = IAQ_Data[3]
            if (CO2 >= CO2_Limit) :
                if CO2_Limit_Flog == 0:
                    IAQ_Cond = "CO2"
                    Send_LineBot(IAQ_Cond,CO2)
                    Send_Iaq()
                    CO2_Limit_Flog = 1
            else :
                if CO2_Limit_Flog == 1:
                    CO2_Limit_Flog = 0
                
            if (TVOC >= TVOC_Limit) :
                if TVOC_Limit_Flog == 0:
                    IAQ_Cond = "TVOC"
                    Send_LineBot(IAQ_Cond,TVOC)
                    Send_Iaq()
                    TVOC_Limit_Flog = 1
            else:
                if TVOC_Limit_Flog == 1:
                    TVOC_Limit_Flog = 0
    except:
        pass


#schedule.every(5).seconds.do(check_Iaq)
schedule.every(10).seconds.do(Send_Iaq)
schedule.every(1).minutes.do(Send_MainPower)
schedule.every(1).minutes.do(Send_SubPower)

'''
schedule.every(5).seconds.do(check_Iaq)
schedule.every(1).minutes.do(Send_Iaq)
schedule.every(1).minutes.do(Send_MainPower)
schedule.every(1).minutes.do(Send_SubPower)
'''


if __name__ == '__main__':
    
    t1 = threading.Thread(target = ipc_subscribe)
    time.sleep(.5)
    t1.start()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    