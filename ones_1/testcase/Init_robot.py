#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/3/30 下午3:47
# @File: Init_robot.py



from packages.logControl import Logging
from API.Matrix_API import MatrixHTTP
from API.Modbus_Api import SR_Pymodbus
from time import sleep


class Init_Robot():
    """
    初始化AGV状态类
    """
    def __init__(self,AGV_IP:str):
        """
        初始化被测AGV
        :param AGV_IP: AGV IP
        """
        try:
            self.logging = Logging('Init_Robot')
            self.AGV_IP = AGV_IP
            try:
                self.matrix = MatrixHTTP(AGV_IP)
                self.modbus = SR_Pymodbus(AGV_IP)
            except BaseException as e:
                self.logging.error('TCP Connection to failed')
        except BaseException as e:
            self.logging.error('__init__: ' + str(e))

    def Check_MatrixLogin(self):
        """
        查询matrix是否能正常登录
        :return:
        """
        try:
            ret = self.matrix.login('admin')
            if ret:
                return True
            else:
                return False
        except BaseException as e:
            self.logging.error('Check_MatrixLogin: ' + str(e))

    def init_robot(self):
        """
        初始化测试AGV状态
        :return:
        """
        try:
            if self.Check_MatrixLogin() == True:
                self.modbus.write_single_coil_function('解除急停')
                sleep(3)
                self.modbus.run_action_task(4,15,0) # 旋转顶升模组回零
                sleep(1)
                i = 0
                while True:
                    sleep(0.5)
                    i += 1
                    if self.modbus.read_input_register_action_status()['action_task_status'] == '执行结束':
                        break
                    else:
                        if i > 1000: self.logging.error('Init_robot failed!'); return 'Init_robot fail!'
                        else:continue
                self.logging.info('Init robot successful')
                return 'Init robot successful'
            else:
                self.logging.error('Failed connect to AGV')
                return 'Failed connect to AGV'
        except BaseException as e:
            self.logging.error('init_robot:' + str(e))