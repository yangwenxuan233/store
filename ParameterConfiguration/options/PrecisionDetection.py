import socket
import time

import matplotlib.pyplot as plt
import numpy as np
from libs.DataStruct import DataStruct


class PrecisionDetection():
    # 精度检测
    def precision_detection():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("192.168.1.77", 8080))
            op, add = s.recvfrom(2048)  # 获取UDP数据
            data = bytearray(op)
            data[4: 5] = DataStruct.struct_pack_one(3)
            data[65: 66] = DataStruct.struct_pack_one(0)  # electrical_machinery_start
            data[577: 578] = DataStruct.struct_pack_one(0)  # adc_code
            data[590: 592] = DataStruct.struct_pack_two('0')  # calibration_mode
            Data = bytes(data)
            s.sendto(Data, add)  # 发送UDP数据包到客户端
            time.sleep(0.5)
            s.close()

            #########################################
            # filepath = 'D:/python/test.csv'  # 数据采集存储路径
            start_angle = 179.95  # 采集起始角度
            end_angle = 180.05  # 采集结束角度
            num = 100  # 采集次数
            #########################################
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("192.168.1.77", 2368))
            Distance = []
            Number = []
            for uu in range(num):
                number = uu + 1
                Number.append(number)
                M = []
                for ii in range(24):
                    data, add = s.recvfrom(2048)  # 获取UDP数据
                    M.append(data)
                for mm in range(24):
                    DATA = M[mm]
                    for jj in range(12):
                        for nn in range(16):
                            angle = int(DataStruct.struct_unpack_two(DATA[jj * 100 + nn * 6 + 2: jj * 100 + nn * 6 + 4])) / 100
                            distance = int(DataStruct.struct_unpack_two(DATA[jj * 100 + nn * 6 + 4: jj * 100 + nn * 6 + 6])) / 4
                            if start_angle < angle <= end_angle:
                                d = distance
                                break
                        if start_angle < angle <= end_angle:
                            break
                Distance.append(d)
            s.close()
            # VAR = np.var(np.array(Distance), ddof=1)
            STD = np.std(np.array(Distance), ddof=1)
            MEAN = np.mean(Distance)
            # RANGE = np.max(Distance) - np.min(Distance)

            # 画图
            fig = plt.figure(figsize=(11.5, 8), dpi=100)
            fig.canvas.manager.window.move(770, 0)
            plt.xlabel('number', size=20)
            plt.ylabel('distance/cm', size=20)
            plt.grid()
            x = np.random.rand(num)
            y = np.random.rand(num)
            z = np.sqrt(x ** 2 + y ** 2)
            plt.scatter(Number, Distance, c=z, s=200, marker='*')
            plt.title(r'Distance_mean: ' + str(round(MEAN, 2)) + '\n' + r'Distance_std: ' + str(round(STD, 2)), size=20, c='b')
            plt.show()
            if STD <= 2:
                return "<font color='green' size='5'><green>检测通过。</font>"
            else:
                return "<font color='red' size='5'><red>超出范围。</font>"
        except Exception as e:
            return "<font color='red' size='5'><red>精度检测失败！" + str(e) + "</font>"
