# -*- coding: utf_8 -*-
# Author: Renxing
# Date: 2022-03-01
# Describe: 用于无线激光测距, 使用前请配置station模式来确定ip和port


import serial
import time
import socket
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


class LaserRang(object):
    def __init__(self):
        self.cmd_list = ['FA040150B1', 'FA0604FC', '500602A8']

    @staticmethod
    def rs458_mod(port):

        try:
            # 用于串口调试， 设定串口为从站
            master = modbus_rtu.RtuMaster(serial.Serial(port=port, baudrate=9600, bytesize=8, parity='N', stopbits=1))
            master.set_timeout(5.0)
            master.set_verbose(True)

            # 读保持寄存器
            read = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 9)  # 这里可以修改需要读取的功能码
            return list(read)
        except Exception as e:
            print("error:", e)

    @staticmethod
    def rs458_serial(port, baud_rate, *cmd):
        try:
            # 用于串口调试，调试前需要串口连接
            ser = serial.Serial(port, baud_rate)
            if ser.is_open:
                print("port open success")
                for i in cmd:
                    ser.write(bytes.fromhex(i))
                    time.sleep(2)  # 延时
                    len_return_data = ser.inWaiting()
                    if len_return_data:
                        return_data = ser.read(len_return_data)  # 读取缓冲数据
                        if len(return_data) > 6:
                            str_return_data = return_data.decode('utf-8', errors='ignore')
                            print("receive str: ", str_return_data)
                        else:
                            str_return_data = str(return_data.hex())
                            print("receive str: ", str_return_data)
                    else:
                        print("Do not get return data, Please check!")
            else:
                print("port open failed")
        except Exception as e:
            print("error :", e)

    def rs458_tcp(self, ip_address, port):
        try:
            address = (ip_address, port)
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_client.settimeout(30)
            tcp_client.connect(address)

            response = None
            for i in self.cmd_list:
                tcp_client.send(bytes.fromhex(i))
                time.sleep(0.1)
                response = tcp_client.recv(1024)
                if not response:
                    response = None
                    # print(f'receive : {response}')
            else:
                return response
        except Exception as e:
            print(e)


def run():
    # 配置ip
    ips = '192.168.33.16'
    # 配置端口
    port = 8899
    # 初始化类
    st = LaserRang()
    # 执行类方法 获取数据
    bytes_val = st.rs458_tcp(ips, port)
    if bytes_val:
        # 对数据进行解码
        str_val = bytes_val.decode('utf-8', errors='ignore')
        # 对特殊字符进行切割
        real_data = str_val.split("")[1]
        print(real_data)


if __name__ == "__main__":
    pass
    # run()
