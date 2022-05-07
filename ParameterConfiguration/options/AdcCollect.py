import os
import socket
import time

import matplotlib.pyplot as plt
import numpy as np
from libs.DataStruct import DataStruct


class AdcCollect():
    # ADC原始数据波形采集
    def adc_collect():
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
            ####################################################
            # 参数
            n = 10
            ####################################################
            # 建立接收连接
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("192.168.1.77", 2368))
            # 画图
            fig = plt.figure(figsize=(11.5, 8), dpi=100)
            fig.canvas.manager.window.move(770, 0)
            plt.xlabel('time/ns', size=20)
            plt.ylabel('amplitude/mv', size=20)
            plt.title('Raw data waveform', size=20)
            x = np.arange(0, 398, 1)
            for ii in range(n):
                data, add = s.recvfrom(2048)  # 获取UDP数据
                y = []
                d_range = np.arange(5, 403, 1)
                for nn in d_range:
                    value = data[nn]
                    if value > 127:
                        value = value - 256
                    value = value * 500 / 127
                    y.append(value)
                plt.plot(x, y)
                # plt.scatter(x, y, c='y')
            s.close()
            plt.grid()
            time_str = time.strftime('%Y%m%d%H%M%S')
            file_name = 'waveform_' + time_str + '.png'
            dirs = 'D:/python/Raw_data_waveform/'
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            plt.savefig(dirs + file_name,  bbox_inches='tight')
            plt.show()
            # time.sleep(5)
            # plt.close('all')
            return "<font color='green' size='5'><green>波形采集完成。</font>"
        except Exception as e:
            return "<font color='red' size='5'><red>波形采集失败!" + str(e) + "</font>"
