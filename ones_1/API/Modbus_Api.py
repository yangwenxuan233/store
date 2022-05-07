# -*- coding:utf-8 -*-
# Standard_Modbus_API:读取AGV状态、控制AGV
# author: weisen
# time:20210827


import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import time
from API.State_analysis import Write_single_coil, Read_Input_register
import json
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from packages.logControl import Logging



class SR_Modbus_tk():

    def __init__(self, ip):
        """
        使用 modbus_tk库读取AGV信息
        """
        self.ip = ip
        self.modbus_tk_client = None
        self.state_analysis = Read_Input_register()  # 状态解析初始化
        # log日志功能初始化
        self.logger = Logging('SR_Pymodbus')
        self.modbus_tcp_connect()

    def modbus_tcp_connect(self):
        """
        modbus_tcp连接
        :return:
        """
        try:
            self.modbus_tk_client = mt.TcpMaster(self.ip, 502)
            self.modbus_tk_client.set_timeout(5.0)  # 设置连接超时时间
        except BaseException as e:
            print('modbus_tcp_connect ERROR:' + str(e))

    def read_register_status(self, starting_address, quantity_of_x) -> int:
        """
        使用功能码04（Read Input Register）进行读取
        :param starting_address: 寄存器地址
        :param quantity_of_x: 读取地址数量
        :return:
        """
        try:
            register_status_data = self.modbus_tk_client.execute(slave=1, function_code=md.READ_INPUT_REGISTERS,
                                                                 starting_address=starting_address,
                                                                 quantity_of_x=quantity_of_x,
                                                                 output_value=5)  # 以元组方式放回
            return register_status_data
        except BaseException as e:
            print('read_register_status ERROR: ' + str(e))

    def decode_uint16(self, value):
        """
        解析无符号16位整型数值
        :param val:数值
        :return:
        """
        try:
            return value
        except BaseException as e:
            print('decode_uint16 ERROR:' + str(e))

    def decode_int16(self, value):
        """
        解析有符号16位整型数值
        :param val:数值
        :return:
        """
        try:
            return -(value & 0x8000) | (value & 0x7fff)
        except BaseException as e:
            print('decode_int16 ERROR: ' + str(e))

    def decode_uint32(self, double_uint16: tuple):
        """
        解析两个16位的寄存器拼成一个32位的,,无符号32位整型数值，大端序（BigEndian）
        :param double_uint16:
        :return:
        """
        num = double_uint16[0] << 16
        num += double_uint16[1]
        return num

    def decode_int32(self, double_uint16: tuple):
        """
        解析有符号32位整型数值，大端序（BigEndian）
        :param double_uint16: 元组数值
        :return:
        """
        try:
            pass
        except BaseException as e:
            print('double_int31 ERROR : ' + str(e))

    def uint32_to_double_uint16(self, uint32):
        """
        一个32位寄存器拆分成两个16的寄存器
        :param uint32:
        :return:
        """
        return [(uint32 >> 16) & 0xFFFF, uint32 & 0xFFFF]


class SR_Pymodbus():

    def __init__(self, ip: str):
        """
        使用pymodbus库读取AGV状态、控制AGV等功能
        :param ip: 车辆ip
        """
        self._client = None
        self.ip = ip
        self.state_analysis = Read_Input_register()  # 状态解析初始化
        self.write_single_function = Write_single_coil()  # 单个线圈功能组初始化
        # log日志功能初始化
        self.logger = Logging('SR_Pymodbus')
        self.pymodbus_connect_tcp()


    def pymodbus_connect_tcp(self):
        """
        pymodbus client TCP方式连接AGV
        :return:
        """
        try:
            self._client = ModbusTcpClient(self.ip, port=502, timeout=3)
            try:
                ret = self._client.connect()
            except BaseException:
                return 'Connection to %s failed' % (self.ip)
            if ret == True:
                return 'Connection succeeded...'
            else:
                return 'Connection to %s failed' % (self.ip)
        except BaseException as e:
            return self.logger.error('pymodbus_connect_tcp :' + str(e))

    def read_input_register(self, address, count):
        """
        重写读取输入寄存器函数功能不解码,功能码04
        :param address: 寄存器地址
        :param count: 线圈数量
        :return:
        """
        try:
            ret = self._client.read_input_registers(address, count, unit=17)
            decoder = BinaryPayloadDecoder.fromRegisters(ret.registers, byteorder=Endian.Big,
                                                         wordorder=Endian.Big)
            return decoder
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_system_status(self):
        """
        读取输入寄存器的系统状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            system_status = self.state_analysis.system_status(
                self.read_input_register(30001, 1).decode_16bit_uint())  # 系统状态
            DI_DO_status = self.read_input_register(30021, 2)
            DI_status = DI_DO_status.decode_16bit_uint()  # DI状态码
            DO_status = DI_DO_status.decode_16bit_uint()  # DO状态码
            error_code = self.read_input_register(30025, 4)
            hardware_error_code = error_code.decode_32bit_uint()  # 硬件故障码
            last_system_error = error_code.decode_32bit_uint()  # 系统上一次故障码
            service_info = self.read_input_register(30041, 6)  # 服务周期
            total_sports_mileage = service_info.decode_32bit_uint()  # 运动总里程
            total_boot_time = service_info.decode_32bit_uint()  # 开机总时间
            total_number_power_on = service_info.decode_32bit_uint()  # 开机总次数
            linux_time = self.read_input_register(30047, 2).decode_32bit_uint()  # linux系统时间戳
            external_ip = self.read_input_register(30049, 4)
            external_ip_address = '{}.{}.{}.{}'.format(external_ip.decode_16bit_uint(), external_ip.decode_16bit_uint(),
                                                       external_ip.decode_16bit_uint(),
                                                       external_ip.decode_16bit_uint())  # 对外通信ip地址
            system_version = self.read_input_register(30053, 3)
            system_version_number = '{}.{}.{}'.format(system_version.decode_16bit_uint(),
                                                      system_version.decode_16bit_uint(),
                                                      system_version.decode_16bit_uint())  # SROS系统版本号
            cur_map_byte_code = self.read_input_register(30065, 1).decode_16bit_uint()  # 当前地图名的前两个字节编码
            system_volume = self.read_input_register(30070, 1).decode_16bit_uint()  # 系统音量
            hardware_error_code_1_5 = self.read_input_register(30081, 10)
            hardware_error_code_1 = hardware_error_code_1_5.decode_32bit_uint()  # 硬件错误码1
            hardware_error_code_2 = hardware_error_code_1_5.decode_32bit_uint()  # 硬件错误码2
            hardware_error_code_3 = hardware_error_code_1_5.decode_32bit_uint()  # 硬件错误码3
            hardware_error_code_4 = hardware_error_code_1_5.decode_32bit_uint()  # 硬件错误码4
            hardware_error_code_5 = hardware_error_code_1_5.decode_32bit_uint()  # 硬件错误码5
            dict_system_status = {
                'current_system_status': system_status,
                'DI_status': DI_status,
                'DO_status': DO_status,
                'hardware_error_code': hardware_error_code,
                'last_system_error': last_system_error,
                'service_info': {
                    'total_sports_mileage': total_sports_mileage,
                    'total_boot_time': total_boot_time,
                    'total_number_power_on': total_number_power_on
                },
                'linux_time': linux_time,
                'external_ip_address': external_ip_address,
                'system_version': system_version_number,
                'cur_map_byte_code': cur_map_byte_code,
                'system_volume': system_volume,
                'hardware_error_code_1_5': {
                    'hardware_error_code_1': hardware_error_code_1,
                    'hardware_error_code_2': hardware_error_code_2,
                    'hardware_error_code_3': hardware_error_code_3,
                    'hardware_error_code_4': hardware_error_code_4,
                    'hardware_error_code_5': hardware_error_code_5
                }
            }
            return dict_system_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_pose_status(self):
        """
        读取输入寄存器的定位状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            positioning_status = self.state_analysis.positioning_status(
                self.read_input_register(30002, 1).decode_16bit_uint())  # 定位状态
            pose = self.read_input_register(30003, 6)
            pose_x = pose.decode_32bit_int()  # 位姿x
            pose_y = pose.decode_32bit_int()  # 位姿y
            pose_yaw = pose.decode_32bit_int()  # 位姿yaw
            pose_confidence = '{}%'.format(
                '%.2f' % ((self.read_input_register(30009, 1).decode_16bit_uint()) * 0.01))  # 位置置信度
            line_speed = self.read_input_register(30017, 3)
            x_line_speed = line_speed.decode_16bit_int() # x方向线速度
            y_line_speed = line_speed.decode_16bit_int() # y方向线速度
            angular_speed = line_speed.decode_16bit_int() # 角速度(1/1000)rad/s
            camera_down = self.read_input_register(30057, 8)
            camera_down_code_id = camera_down.decode_32bit_int()  # 下视PGV扫描到的二维码ID
            camera_down_code_x = camera_down.decode_32bit_int()  # 下视PGV扫描到的二维码x
            camera_down_code_y = camera_down.decode_32bit_int()  # 下视PGV扫描到的二维码y
            camera_down_code_yaw = camera_down.decode_32bit_int()  # 下视PGV扫描到的二维码yaw
            # 封装成json格式
            dict_pose_status = {
                'positioning_status': positioning_status,
                'pose_confidence': pose_confidence,
                'pose': {
                    "pose_x": pose_x,
                    'pose_y': pose_y,
                    'pose_yaw': pose_yaw
                },
                'real_time_speed':{
                    'x_line_speed':x_line_speed,
                    'y_line_speed':y_line_speed,
                    'angular_speed':angular_speed
                },
                'camera_down': {
                    'camera_down_code_id': camera_down_code_id,
                    'camera_down_code_x': camera_down_code_x,
                    'camera_down_code_y': camera_down_code_y,
                    'camera_down_code_yaw': camera_down_code_yaw
                }
            }
            return dict_pose_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_action_status(self):
        """
        读取输入寄存器的动作状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            action_task_status = self.state_analysis.action_task_status(
                self.read_input_register(30129, 1).decode_16bit_uint())  # 动作任务状态
            actiom_task = self.read_input_register(30130, 8)
            actiom_task_no = actiom_task.decode_32bit_int()
            actiom_task_ID = actiom_task.decode_32bit_int()
            actiom_task_parameter_0 = actiom_task.decode_32bit_int()
            actiom_task_parameter_1 = actiom_task.decode_32bit_int()
            action_task_result_data = self.read_input_register(30138, 3)
            action_task_result = self.state_analysis.action_task_result(action_task_result_data.decode_16bit_uint())
            action_task_result_value = action_task_result_data.decode_32bit_int()
            dict_action_status = {
                'action_task_status': action_task_status,
                'actiom_task': {
                    'actiom_task_no': actiom_task_no,
                    'actiom_task_ID': actiom_task_ID,
                    'actiom_task_parameter_0': actiom_task_parameter_0,
                    'actiom_task_parameter_1': actiom_task_parameter_1,
                    'action_task_result': action_task_result,
                    'action_task_result_value': action_task_result_value
                }
            }
            return dict_action_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_move_status(self):
        """
        读取输入寄存器的移动状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            move_task_status = self.state_analysis.mobile_task_status(
                self.read_input_register(30113, 1).decode_16bit_uint())  # 移动任务状态
            move_task_no = self.read_input_register(30114, 2).decode_32bit_int()
            move_task = self.read_input_register(30116, 2)
            move_task_target_site = move_task.decode_16bit_uint()  # 移动任务目标站点
            move_task_path_number = move_task.decode_16bit_uint()  # 当前路径编号，移动任务运行过程中有效
            move_task_result_value = self.read_input_register(30122, 3)
            move_task_result = self.state_analysis.mobile_task_result(
                move_task_result_value.decode_16bit_uint())  # 移动任务结果
            move_task_value = move_task_result_value.decode_32bit_uint()  # 移动任务结果值
            dict_move_status = {
                'move_task_status': move_task_status,
                'move_task': {
                    'move_task_no': move_task_no,
                    'move_task_target_site': move_task_target_site,
                    'move_task_path_number': move_task_path_number,
                    'move_task_result': move_task_result,
                    'move_task_value': move_task_value
                }
            }
            return dict_move_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_mission_status(self):
        """
        读取输入寄存器的mission状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            running_mission_id = self.read_input_register(30097, 2).decode_32bit_uint()  # 正在运行mission_id
            mission_task = self.read_input_register(30099, 2)
            mission_task_status = self.state_analysis.mission_operating_status(
                mission_task.decode_16bit_uint())  # mission 运行状态
            mission_task_result = self.state_analysis.mission_operating_result(
                mission_task.decode_16bit_uint())  # mission 执行结果
            mission_error_code = self.read_input_register(30101, 2).decode_32bit_uint()  # mission 任务错误码
            dict_mission_status = {
                'running_mission_id': running_mission_id,
                'mission_task_status': mission_task_status,
                'mission_task_result': mission_task_result,
                'mission_error_code': mission_error_code
            }
            return dict_mission_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_battery_status(self):
        """
        读取输入寄存器的电池状态的值并直接解析数据，重组dict格式返回
        :return:
        """
        try:
            battery_info = self.read_input_register(30033, 8)
            battery_voltage = '{}'.format('%.2f' % (battery_info.decode_16bit_uint() * 0.001))  # 电池电压V
            battery_current = '{}'.format('%.2f' % (battery_info.decode_16bit_int() * 0.001))  # 电池电流A（负数为充电电流）
            battery_temperature = battery_info.decode_16bit_int()  # 电池温度℃
            battery_remain_time = '{}'.format('%.2f' % (battery_info.decode_16bit_uint() / 60))  # 电池预计使用时间h
            battery_percentage_electricity = battery_info.decode_16bit_uint()  # 当前电量百分比【1，100】
            battery_state = self.state_analysis.battery_info_state(battery_info.decode_16bit_uint())  # 当前电池状态
            battery_use_cycles = battery_info.decode_16bit_uint()  # 电池循环次数
            battery_nominal_capacity = battery_info.decode_16bit_uint()  # 电池标称容量mAh
            dict_battery_status = {
                'battery_voltage(V)': battery_voltage,
                'battery_current(A)': battery_current,
                'battery_temperature(℃）': battery_temperature,
                'battery_remain_time（h)': battery_remain_time,
                'battery_percentage_electricity': battery_percentage_electricity,
                'battery_state': battery_state,
                'battery_use_cycles': battery_use_cycles,
                'battery_nominal_capacity(mAh)': battery_nominal_capacity
            }
            return dict_battery_status
        except BaseException as e:
            self.logger.error(e)

    def read_input_register_all_status(self):
        """
        读取输入寄存器的全部状态，重组json格式返回,0.5s时间返回
        :return:
        """
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dict_all_status = {
                'current_time': current_time,
                'system_status': self.read_input_register_system_status(),
                'battery_status': self.read_input_register_battery_status(),
                'pose_status': self.read_input_register_pose_status(),
                'action_status': self.read_input_register_action_status(),
                'move_status': self.read_input_register_move_status(),
                'mission_status': self.read_input_register_mission_status(),
            }
            json_msg = json.dumps(dict_all_status, ensure_ascii=False, indent=2, sort_keys=False)  # 装载json
            return json_msg
        except BaseException as e:
            self.logger.error(e)

    def read_discrete_inputs(self, address) -> bool:
        """
        读取离量输入状态，功能码02,返回bool值
        :param address: 寄存器地址
        :return:
        """
        result = self._client.read_discrete_inputs(address, unit=17)
        ret = result.getBit(0)
        return ret

    def read_discrete_inputs_all_status(self):
        """
        一次性读取离散量系统状态（功能码02 Read Discrete Inputs），返回值格式：json
        :return:
        """
        try:
            emergency_stop_is_triggered = self.read_discrete_inputs(10001)  # 急停是否触发
            emergency_stop_can_be_recovered = self.read_discrete_inputs(10002)  # 急停是否可恢复
            is_open_brake = self.read_discrete_inputs(10003)  # 是否抱闸
            is_it_charging = self.read_discrete_inputs(10004)  # 是否正在充电
            is_low_power_mode = self.read_discrete_inputs(10005)  # 是否处于低功率模式
            is_obstacles_to_slow = self.read_discrete_inputs(10006)  # 是否遇到障碍物减速
            is_obstacles_to_pause = self.read_discrete_inputs(10007)  # 是否遇到障碍物暂停
            is_ready_for_movement_task = self.read_discrete_inputs(10009)  # 当前是否可以运行移动任务
            # DI_0 = self.read_discrete_inputs(10017)
            # DI_1 = self.read_discrete_inputs(10018)
            # DI_2 = self.read_discrete_inputs(10019)
            # DI_3 = self.read_discrete_inputs(10020)
            # DI_4 = self.read_discrete_inputs(10021)
            # DI_5 = self.read_discrete_inputs(10022)
            # DI_6 = self.read_discrete_inputs(10023)
            # DI_7 = self.read_discrete_inputs(10023)
            # DO_0 = self.read_discrete_inputs(10033)
            # DO_1 = self.read_discrete_inputs(10034)
            # DO_2 = self.read_discrete_inputs(10035)
            # DO_3 = self.read_discrete_inputs(10036)
            # DO_4 = self.read_discrete_inputs(10037)
            # DO_5 = self.read_discrete_inputs(10038)
            # DO_6 = self.read_discrete_inputs(10039)
            # DO_7 = self.read_driscrete_inputs(10040)
            release_statue = self.read_discrete_inputs(10049)
            is_in_scheduling_mode = self.read_discrete_inputs(10051)
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dict_all_status = {
                'current_time': current_time,
                'emergency_stop_is_triggered ': emergency_stop_is_triggered,
                'emergency_stop_can_be_recovered': emergency_stop_can_be_recovered,
                'is_open_brake': is_open_brake,
                'is_it_charging': is_it_charging,
                'is_low_power_mode': is_low_power_mode,
                'is_obstacles_to_slow': is_obstacles_to_slow,
                'is_obstacles_to_pause': is_obstacles_to_pause,
                'is_ready_for_movement_task': is_ready_for_movement_task,
                'release_statue': release_statue,
                'is_in_scheduling_mode': is_in_scheduling_mode
            }
            json_msg = json.dumps(dict_all_status, ensure_ascii=False, indent=2, sort_keys=False)  # 装载json
            return json_msg
        except BaseException as e:
            self.logger.error(e)

    def write_single_coil(self, address, value):
        """
        使用功能码0x05写入写单个线圈,value:写入值，0代表写入:0x0000,1代表写入:0xFF00
        :param address:寄存器地址
        :param value:写入值，0:0x0000,1:0xFF00
        :return:
        """
        try:
            if value == 0:
                self._client.write_coil(address, 0x0000, unit=17)
            else:
                self._client.write_coil(address, 0xFF00, unit=17)
        except BaseException as e:
            self.logger.error(e)

    def write_single_coil_function(self, function: str):
        """
        根据传入功能写入功能值,详见功能组列表：self.write_single_function = State_analysis.Write_single_coil()
        例：self.write_single_coil_function('触发急停')
        :param function: 功能名称，详见功能组列表：self.write_single_function = State_analysis.Write_single_coil()
        :return:
        """
        try:
            function_address = self.write_single_function.functional_group(function)
            self.write_single_coil(function_address, 1)
        except BaseException as e:
            self.logger.error(e)

    def write_single_coil_function_scheduling_mode(self, function: int):
        """
        开启或者关闭调度模式，1：开启，0：关闭
        :param function: 开启或者关闭 1：开启，0：关闭
        :return:
        """
        try:
            if function == 1:
                self.write_single_coil(51, 1)
            else:
                self.write_single_coil(51, 0)
        except BaseException as e:
            self.logger.error(e)

    def write_single_coil_function_obstacle_avoidance_area(self, function: int):
        """
        开启或者关闭屏蔽避障区域，1：开启，0：关闭
        :param function: 1：开启，0：关闭
        :return:
        """
        try:
            if function == 1:
                self.write_single_coil(6, 1)
            else:
                self.write_single_coil(6, 0)
        except BaseException as e:
            self.logger.error(e)

    def use_pose_positioning(self, x, y, yaw) -> int:
        """
        通过位姿进行定位
        :param x: x方向(mm)
        :param y: y方向(mm)
        :param yaw: yaw方向（1/1000）rad
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_int(x)
            builder.add_32bit_int(y)
            builder.add_32bit_int(yaw)
            self._client.write_registers(40001, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def use_site_positioning(self, site: int):
        """
        通过站点定位
        :param site:
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(site)
            self._client.write_registers(40007, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def freely_navigate_to_site(self, site: int):
        """
        自主导航移动到站点
        :param site:站点
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(site)
            self._client.write_registers(40015, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def set_obstacle_avoidance_strategy(self, value: int):
        """
        设置避障策略，0x01:暂停运动直至障碍消失
        0x02:重新规划路径绕过障碍
        0x10:不避障（可能导致事故，谨慎使用，自由导航有效）
        :param value:1，2，3
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(value)
            self._client.write_registers(40016, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def use_manual_control(self, Vx, Vy, Vyaw) -> int:
        """
        手动控制车辆运行，需要在手动模式才生效；每次只执行100ms若要连续运行需要不间断发送
        :param Vx:单位mm/s(前进为正，后退为负）
        :param Vy:单位mm/s
        :param Vyaw:单位(1/1000)rad/s（向左边为正，向右为负）
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_int(Vx)
            builder.add_16bit_int(Vy)
            builder.add_16bit_int(Vyaw)
            self._client.write_registers(40022, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def set_speed_level(self, level: int):
        """
        设置速度级别
        :param level:速度级别[1,100]
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(level)
            self._client.write_registers(40026, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def set_speaker_volume(self, volume: int):
        """
        设置系统扬声器音量[1,100]
        :param volume: 音量
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(volume)
            self._client.write_registers(40028, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def set_GPIO_output(self, value: int):
        """
        设置GPIO_output的值
        :param value:输出值
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(value)
            builder.add_16bit_uint(0xFFFF)
            self._client.write_registers(40030, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def set_mission_general_register(self, number: int):
        """
        设置mission中的通用寄存器0--7
        :param number:寄存器序号：0--7
        :return:
        """
        try:
            general_register_address = 40033 + number  # 通用寄存器地址
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_uint(0)
            self._client.write_registers(general_register_address, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def use_forced_pose_positioning(self, x, y, yaw) -> int:
        """
        通过位姿强制定位
        :param x: x方向（mm）
        :param y: y方向（mm）
        :param yaw: yaw方向（(1/1000)rad）
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_int(x)
            builder.add_32bit_int(y)
            builder.add_32bit_int(yaw)
            self._client.write_registers(40049, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def free_navigation_pose(self, x, y, yaw, no=0) -> int:
        """
        自由导航到位置
        :param x: x方向（mm）
        :param y: y方向（mm）
        :param yaw: yaw方向（(1/1000)rad
        :param no: 任务编号
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_int(no)
            builder.add_32bit_int(x)
            builder.add_32bit_int(y)
            builder.add_32bit_int(yaw)
            self._client.write_registers(40059, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def free_navigation_move_site(self, site, no=0) -> int:
        """
        自由导航移动到站点
        :param site: 站点
        :param no: 任务编号
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_int(no)
            builder.add_16bit_uint(site)
            self._client.write_registers(40066, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def run_action_task(self, id, parameter0, parameter1, no=0) -> int:
        """
        执行动作任务,例如 :执行4-1-0：self.run_action_task(4,1,0)
        :param id: 执行动作任务ID
        :param parameter0:执行动作任务参数0
        :param parameter1:执行动作任务参数1
        :param no:执行动作任务编号
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_int(no)
            builder.add_32bit_int(id)
            builder.add_32bit_int(parameter0)
            builder.add_32bit_int(parameter1)
            self._client.write_registers(40070, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)

    def run_mission_task(self, id: int):
        """
        执行mission任务
        :param id: 任务id，可在mattrix查看
        :return:
        """
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_uint(id)
            self._client.write_registers(40097, builder.to_registers(), unit=17)
        except BaseException as e:
            self.logger.error(e)