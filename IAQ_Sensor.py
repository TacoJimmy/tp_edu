
import codecs
# -*- coding: UTF-8 -*-

import time 
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import struct


def int16_pair_to_float(num1, num2):
    combined_num = (num1 << 16) | num2
    packed_num = struct.pack('i', combined_num)
    float_num = struct.unpack('f', packed_num)[0]
    return float_num

def Read_IAQ(id):
    try:
        global master
        master = modbus_tcp.TcpMaster(host="192.168.1.110")
        master.set_timeout(5.0)
        IAQ_Data = master.execute(id, cst.READ_HOLDING_REGISTERS, 0, 20)
        
        CO2 = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
        TVOC = round(int16_pair_to_float(IAQ_Data[3], IAQ_Data[2]))
        Temp = round(int16_pair_to_float(IAQ_Data[5], IAQ_Data[4]),1)
        Humi = round(int16_pair_to_float(IAQ_Data[7], IAQ_Data[6]),1)
        time.sleep(1)
        return CO2,TVOC,Temp,Humi
    except:
        pass

def Read_CO2Limit():
    try:
        global master
        master = modbus_tcp.TcpMaster(host="192.168.1.110")
        master.set_timeout(5.0)
        IAQ_Data = master.execute(1, cst.READ_HOLDING_REGISTERS, 8, 2)
        CO2_Limit = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
        time.sleep(1)
        return CO2_Limit
    except:
        return "error"

def Read_TVOCLimit():
    try:
        global master
        master = modbus_tcp.TcpMaster(host="192.168.1.110")
        master.set_timeout(5.0)
        IAQ_Data = master.execute(1, cst.READ_HOLDING_REGISTERS, 10, 2)
        TVOCLimit = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
        time.sleep(1)
        return TVOCLimit
    except:
        return "error"

def write_CO2_Limit(CO2Limet_Value):
    global master
    try:
        if (CO2Limet_Value >= 200) & (CO2Limet_Value <= 2000):
            master = modbus_tcp.TcpMaster(host="192.168.1.110")
            master.set_timeout(5.0)
            print (master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 9, output_value=[CO2Limet_Value],data_format='!f'))
            time.sleep(1)
            #IAQ_Data = master.execute(1, cst.READ_HOLDING_REGISTERS, 8, data_format='!f')
            #CO2_Limit = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
            #print (IAQ_Data)
            time.sleep(1)
        else:
            print("Input_error")
    except:
        pass
        
def write_TVOC_Limit(TVOCLimet_Value):
    global master
    try:
        if (TVOCLimet_Value >= 50) & (TVOCLimet_Value <= 300):
            master = modbus_tcp.TcpMaster(host="192.168.1.110")
            master.set_timeout(5.0)
            print (master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 11, output_value=[TVOCLimet_Value],data_format='!f'))
            time.sleep(1)
            #IAQ_Data = master.execute(1, cst.READ_HOLDING_REGISTERS, 8, data_format='!f')
            #CO2_Limit = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
            #print (IAQ_Data)
            time.sleep(1)
    except:
        pass

if __name__ == '__main__':
    write_CO2_Limit(1000)
    print (Read_CO2Limit())
    write_TVOC_Limit(90)
    print (Read_TVOCLimit())
    #print(Read_IAQ(1))
    #write_CO2_Limit(0,17530)
    #print (Read_CO2Limit())
    
    
