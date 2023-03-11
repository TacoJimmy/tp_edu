import struct

def int16_pair_to_float(num1, num2):
    """將兩個int16數值轉換為浮點數"""
    # 將兩個int16組合成一個int32
    combined_num = (num1 << 16) | num2
    # 使用 struct.pack() 將int32轉換為bytes
    packed_num = struct.pack('i', combined_num)
    # 使用 struct.unpack() 將bytes轉換為浮點數
    float_num = struct.unpack('f', packed_num)[0]
    return float_num

# 測試程式碼
num1 = 17530
num2 = 0
float_num = int16_pair_to_float(num1, num2)
print(float_num)  # 1000.0