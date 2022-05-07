import socket

from config.ParameterSettings import ParameterSettings
from libs.DataStruct import DataStruct


class SetParameter():
    # 配置设备参数
    def set_parameter(list):
        if list != []:
            # 获取数据格式
            base_bytes = ParameterSettings.base_bytes
            # 获取数据长度
            base_parameter = ParameterSettings.base_parameter
            # 获取原始地址
            base_add = ParameterSettings.base_add

            # 数据打包
            try:
                # 开放参数
                list[0] = DataStruct.struct_pack_one(3)  # configuration_pattern
                list[1] = DataStruct.struct_pack_two(list[1])  # hw_version
                list[2] = DataStruct.struct_pack_four_ip(list[2])  # fpga_version
                list[3] = DataStruct.struct_pack_two(list[3])  # practical_velocity
                list[4] = DataStruct.struct_pack_two(str(int(float(list[4]) / 101 / 3.3 * 4096 + 0.5)))  # apd_vol
                list[5] = DataStruct.struct_pack_two(str(int((int(list[5]) * 10 + 500) / 3300 * 4096 + 0.5)))  # temperature
                list[6] = DataStruct.struct_pack_six(list[6])  # gps_time
                list[7] = DataStruct.struct_pack_two(list[7])  # intervl_time
                list[8] = DataStruct.struct_pack_two(list[8])  # near_filter_value
                list[9] = DataStruct.struct_pack_two(list[9])  # near_filter_distance
                list[10] = DataStruct.struct_pack_two(list[10])  # far_filter_value
                list[11] = DataStruct.struct_pack_two(list[11])  # far_filter_distance
                list[12] = DataStruct.struct_pack_one(list[12])  # electrical_machinery_start
                list[13] = DataStruct.struct_pack_two(list[13])  # elec_mach_velocity
                list[14] = DataStruct.struct_pack_two(list[14])  # laser_frequency
                list[15] = DataStruct.struct_pack_four_ip(list[15])  # local_IP
                list[16] = DataStruct.struct_pack_four_ip(list[16])  # remote_IP
                list[17] = DataStruct.struct_pack_two(list[17])  # pc_port
                list[18] = DataStruct.struct_pack_two(list[18])  # device_port
                list[19] = DataStruct.struct_pack_mac(list[19])  # device_MAC

                # 配置参数
                list[20] = DataStruct.struct_pack_sn(list[20])  # sn_code
                list[21] = DataStruct.struct_pack_two(list[21])  # voltage_value
                list[22] = DataStruct.struct_pack_two(list[22])  # x1
                list[23] = DataStruct.struct_pack_two(list[23])  # x2
                list[24] = DataStruct.struct_pack_two(list[24])  # x3
                list[25] = DataStruct.struct_pack_two(list[25])  # x4
                list[26] = DataStruct.struct_pack_two(list[26])  # x5
                list[27] = DataStruct.struct_pack_two(list[27])  # x6
                list[28] = DataStruct.struct_pack_two(list[28])  # k1
                list[29] = DataStruct.struct_pack_two(list[29])  # k2
                list[30] = DataStruct.struct_pack_two(list[30])  # k3
                list[31] = DataStruct.struct_pack_two(list[31])  # k4
                list[32] = DataStruct.struct_pack_two(list[32])  # k5
                list[33] = DataStruct.struct_pack_two(list[33])  # k6
                list[34] = DataStruct.struct_pack_two(list[34])  # threshold_value1
                list[35] = DataStruct.struct_pack_two(list[35])  # threshold_value2

                list[36] = DataStruct.struct_pack_two(str(int(int(list[36]) / 15 * 256 + 0.5)))  # distance_start
                list[37] = DataStruct.struct_pack_two(str(int(float(list[37])*256)))  # secondary_distance
                list[38] = DataStruct.struct_pack_two(str(int(float(list[38]) * 100)))  # angle_deviant
                list[39] = DataStruct.struct_pack_two(str(int(float(list[39]) * 100)))  # angle_initial_value
                list[40] = DataStruct.struct_pack_one(list[40])  # apd_temperature_coefficient
                list[41] = DataStruct.struct_pack_one(str(int(int(list[41])/15*256 + 0.5)))  # near_distance_compensation
                list[42] = DataStruct.struct_pack_one(list[42])  # adc_code
                list[43] = DataStruct.struct_pack_two(list[43])  # one_angle_decide
                list[44] = DataStruct.struct_pack_two(list[44])  # two_angle_decide
                list[45] = DataStruct.struct_pack_two(list[45])  # three_angle_decide
                list[46] = DataStruct.struct_pack_two(list[46])  # std_decide
                list[47] = DataStruct.struct_pack_two(list[47])  # near_distance_threshold
                list[48] = DataStruct.struct_pack_two(list[48])  # near_distance_decide
                list[49] = DataStruct.struct_pack_two(list[49])  # calibration_mode

                # 数据拼合
                list_generator = (i for i in list)
                i = 0
                for key in base_parameter:
                    if key.startswith('null'):
                        i += base_parameter[key]
                    else:
                        base_bytes[i: i + base_parameter[key]] = next(list_generator)
                        i += base_parameter[key]

                Data = bytes(base_bytes)
                # 数据发送
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind(("192.168.1.77", 8080))  # 本机IP，端口
                s.sendto(Data, base_add)  # 发送UDP数据包到客户端
                s.close()
                return "<font color='green' size='5'><green>参数配置成功。</font>"
            except Exception as e:
                return "<font color='red' size='5'><red>参数配置失败!" + str(e) + "</font>"
        else:
            return "<font color='red' size='5'><red>参数为空，请配置参数!</font>"
