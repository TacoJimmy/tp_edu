
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
        master = modbus_tcp.TcpMaster(host="192.168.2.110")
        master.set_timeout(5.0)
        IAQ_Data = master.execute(id, cst.READ_HOLDING_REGISTERS, 0, 20)
        CO2 = round(int16_pair_to_float(IAQ_Data[1], IAQ_Data[0]))
        PM25 = round(int16_pair_to_float(IAQ_Data[3], IAQ_Data[2]))
        PM10 = round(int16_pair_to_float(IAQ_Data[5], IAQ_Data[4]))
        CO = round(int16_pair_to_float(IAQ_Data[7], IAQ_Data[6]))
        HCHO = round(int16_pair_to_float(IAQ_Data[9], IAQ_Data[8]),2)
        ammonia = round(int16_pair_to_float(IAQ_Data[11], IAQ_Data[10]),1)
        O2 = round(int16_pair_to_float(IAQ_Data[13], IAQ_Data[12]),2)
        TVOC = round(int16_pair_to_float(IAQ_Data[15], IAQ_Data[14]))
        Temp = round(int16_pair_to_float(IAQ_Data[17], IAQ_Data[16]),2)
        Humi = round(int16_pair_to_float(IAQ_Data[19], IAQ_Data[18]),2)
        time.sleep(1)
        return CO2,PM25,PM10,CO,HCHO,ammonia,O2,TVOC,Temp,Humi
    except:
        pass

if __name__ == '__main__':
    print (Read_IAQ(1))
