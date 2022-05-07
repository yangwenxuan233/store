import socket
from copy import deepcopy

from config.ParameterSettings import ParameterSettings
from libs.DataStruct import DataStruct


class ReadParameter():
    # 读取设备参数
    def read_parameter():
        # 建立接收连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(("192.168.1.77", 8080))
            data, add = s.recvfrom(2048)  # 获取UDP数据
        except Exception:
            s.close()
            data = []
            return "<font color='red' size='5'><red>请求地址无效，上位机连接超时!</font>"

        # 开放参数
        if data != []:
            generator = DataStruct.read_generator(data, ParameterSettings.base_parameter)
            new_dict = deepcopy(ParameterSettings.base_parameter)
            for i in new_dict:
                try:
                    new_dict[i] = next(generator)
                except StopIteration:
                    return "<font color='red' size='5'><red>数据分割失败!</font>"

            try:
                # 字节流转字符串
                Configuration_pattern = DataStruct.struct_unpack_one(new_dict['配置模式'])
                Hw_version = DataStruct.struct_unpack_two(new_dict['硬件版本号'])
                Fpga_version = DataStruct.struct_inpack_ip(new_dict['FPGA版本号'])
                Practical_velocity = DataStruct.struct_unpack_two(new_dict['电机实时转速'])
                Apd_vol = str(int(int(DataStruct.struct_unpack_two(new_dict['APD高压'])) / 4096 * 3.3 * 101 * 10) / 10)
                Temperature = str(int((int(DataStruct.struct_unpack_two(new_dict['温度'])) / 4096 * 3300 - 500) / 10))
                Gps_time = DataStruct.struct_unpack_six(new_dict['GPS时间'])
                Intervl_time = DataStruct.struct_unpack_two(new_dict['间隔时间'])
                Near_filter_value = DataStruct.struct_unpack_two(new_dict['近距滤波值'])
                Near_filter_distance = DataStruct.struct_unpack_two(new_dict['近距滤波距离'])
                Far_filter_value = DataStruct.struct_unpack_two(new_dict['远距滤波值'])
                Far_filter_distance = DataStruct.struct_unpack_two(new_dict['远距滤波距离'])
                Electrical_machinery_start = DataStruct.struct_unpack_one(new_dict['启停电机'])
                Elec_mach_velocity = DataStruct.struct_unpack_two(new_dict['电机速度'])
                Laser_frequency = DataStruct.struct_unpack_two(new_dict['点频选择'])
                Local_IP = DataStruct.struct_inpack_ip(new_dict['LocalIP'])
                Remote_IP = DataStruct.struct_inpack_ip(new_dict['RemoteIP'])
                Pc_port = DataStruct.struct_unpack_two(new_dict['数据端口'])
                Device_port = DataStruct.struct_unpack_two(new_dict['设备端口'])
                Device_MAC = DataStruct.struct_unpack_mac(new_dict['设备mac地址'])
                # 配置参数
                SN_code = DataStruct.struct_unpack_sn(new_dict['序列号（SN）'])
                Threshold_value1 = DataStruct.struct_unpack_two(new_dict['阈值1'])
                Threshold_value2 = DataStruct.struct_unpack_two(new_dict['阈值2'])
                Voltage_value = DataStruct.struct_unpack_two_APD_Vol(new_dict['高压偏移参数'])
                X1 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X1'])
                X2 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X2'])
                X3 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X3'])
                X4 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X4'])
                K1 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K1'])
                K2 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K2'])
                K3 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K3'])
                K4 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K4'])
                X5 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X5'])
                X6 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:X6'])
                K5 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K5'])
                K6 = DataStruct.struct_unpack_two(new_dict['脉宽补偿:K6'])
                Distance_start = str(int(int(DataStruct.struct_unpack_two(new_dict['初始补偿距离'])) / 256 * 15))
                Secondary_distance = str(int(DataStruct.struct_unpack_two(new_dict['二级补偿距离']))/256)
                Angle_deviant = str(int(DataStruct.struct_unpack_two_APD_Vol(new_dict['角度偏移值'])) / 100)
                Angle_initial_value = str(int(DataStruct.struct_unpack_two(new_dict['盲区开角度数'])) / 100)
                Apd_temperature_coefficient = DataStruct.struct_unpack_one(new_dict['APD温度系数'])
                Near_distance_compensation = str(int(int(DataStruct.struct_unpack_one(new_dict['弱信号补偿']))/256*15))
                ADC_data = DataStruct.struct_unpack_one(new_dict['ADC原始数据模式'])
                One_angle_decide = DataStruct.struct_unpack_two(new_dict['一级角度判定阈值'])
                Two_angle_decide = DataStruct.struct_unpack_two(new_dict['二级角度判定阈值'])
                Three_angle_decide = DataStruct.struct_unpack_two(new_dict['三级角度判定阈值'])
                Std_decide = DataStruct.struct_unpack_two(new_dict['方差判定阈值'])
                Near_distance_threshold = DataStruct.struct_unpack_two(new_dict['近距弱信号能量阈值'])
                Near_distance_decide = DataStruct.struct_unpack_two(new_dict['近距弱信号判定距离'])
                Calibration_mode = DataStruct.struct_unpack_two(new_dict['校准debug模式'])

            except Exception as e:
                print(e)
                return "<font color='red' size='5'><red>参数解包失败!" + str(e) + "</font>"

        return (Configuration_pattern,  Hw_version,  Fpga_version, Practical_velocity, Apd_vol,
                Temperature, Gps_time, Intervl_time, Near_filter_value, Near_filter_distance,
                Far_filter_value, Far_filter_distance, Electrical_machinery_start, Elec_mach_velocity,
                Laser_frequency, Local_IP, Remote_IP, Pc_port, Device_port, Device_MAC,
                SN_code, Threshold_value1, Threshold_value2, Voltage_value,
                X1, X2, X3, X4, K1, K2, K3, K4, X5, X6, K5, K6, Distance_start, Secondary_distance, Angle_deviant,
                Angle_initial_value, Apd_temperature_coefficient, Near_distance_compensation,  ADC_data,
                One_angle_decide, Two_angle_decide, Three_angle_decide, Std_decide, Near_distance_threshold,
                Near_distance_decide, Calibration_mode)
