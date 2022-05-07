import socket
import time

import numpy as np
from libs.DataStruct import DataStruct


class EnergyDetection():
    # 能量检测
    def energy_detection():
        def energy_number():
            #########################################
            start_angle = 179.95  # 采集起始角度
            end_angle = 180.05  # 采集结束角度
            num = 10  # 采集次数
            #########################################

            # 参数设置
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

            # 能量采集
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("192.168.1.77", 2368))
            Energy = []
            for uu in range(num):
                M = []
                for ii in range(24):
                    data, add = s.recvfrom(2048)  # 获取UDP数据
                    M.append(data)
                for mm in range(24):
                    DATA = M[mm]
                    for jj in range(12):
                        for nn in range(16):
                            angle = int(DataStruct.struct_unpack_two(DATA[jj * 100 + nn * 6 + 2: jj * 100 + nn * 6 + 4])) / 100
                            energy = int(DataStruct.struct_unpack_two(DATA[jj * 100 + nn * 6 + 6: jj * 100 + nn * 6 + 8]))
                            if start_angle < angle <= end_angle:
                                eng = energy
                                break
                    if start_angle < angle <= end_angle:
                        break
                Energy.append(eng)
            s.close()
            MEAN = np.mean(Energy)
            return MEAN

        try:
            MEAN = energy_number()
            acc_apd_vol = 0
            if 950 <= MEAN <= 1050:
                return "<font color='green' size='5'><green>能量合格。</font>"
            while MEAN < 950:
                acc_apd_vol = acc_apd_vol + 1
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind(("192.168.1.77", 8080))
                op, add = s.recvfrom(2048)  # 获取UDP数据
                data = bytearray(op)
                data[4: 5] = DataStruct.struct_pack_one(3)
                data[545: 547] = DataStruct.struct_pack_two(str(acc_apd_vol))  # voltage_value
                Data = bytes(data)
                s.sendto(Data, add)  # 发送UDP数据包到客户端
                time.sleep(1)
                s.close()
                MEAN = energy_number()
                if acc_apd_vol < 5:
                    return "<font color='green' size='5'><green>能量合格。</font>"
                else:
                    break
            if MEAN < 950:
                return "<font color='red' size='5'><red>能量过低。</font>"

            while MEAN > 1050:
                acc_apd_vol = acc_apd_vol - 1
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind(("192.168.1.77", 8080))
                op, add = s.recvfrom(2048)  # 获取UDP数据
                data = bytearray(op)
                data[4: 5] = DataStruct.struct_pack_one(3)
                data[545: 547] = DataStruct.struct_pack_two(str(acc_apd_vol))  # voltage_value
                Data = bytes(data)
                s.sendto(Data, add)  # 发送UDP数据包到客户端
                time.sleep(1)
                s.close()
                MEAN = energy_number()
                if acc_apd_vol > -5:
                    return "<font color='green' size='5'><green>能量合格。</font>"
                else:
                    break
            if MEAN > 1050:
                return "<font color='red' size='5'><red>能量过高。</font>"
        except Exception as e:
            return "<font color='red' size='5'><red>能量检测失败！" + str(e) + "</font>"
