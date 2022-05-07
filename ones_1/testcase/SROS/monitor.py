#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ywx
# @Modify: add testcases
# @Time: 2022/4/20 16:51


from API.Matrix_API import MatrixHTTP
from API.Modbus_Api import SR_Pymodbus
from packages.caseResult import CaseResult
from packages.logControl import Logging


class TestCase:

    def __init__(self, parameter):
        self.parameter = parameter
        self.logger = Logging('monitor')
        self.matrix = MatrixHTTP(self.parameter['AGV_IP'])
        self.result = CaseResult(parameter['task_uuid'])
        self.ip = self.parameter['AGV_IP']
        self.modbus = SR_Pymodbus(self.ip)

    def case4091(self):
        '''
        title: 电量
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_percentage_electricity'])
            self.logger.info('battery_percentage_electricity ' + str(result))
            if result > 0 and result <= 100:
                return self.result.caseResult('passed', f'case4091:{result}')
            else:
                return self.result.caseResult('failed', f'case4091:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4091:{e}')

    def case4092(self):
        '''
        title: 温度
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_temperature(℃）'])
            self.logger.info('battery_temperature(℃)' + str(result))
            if result > 0 and result <= 100:
                return self.result.caseResult('passed', f'case4091:{result}')
            else:
                return self.result.caseResult('failed', f'case4091:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4091:{e}')

    def case4093(self):
        '''
        title: 电压
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_voltage(V)'])
            self.logger.info('battery_voltage(V) ' + str(result))
            if result > 0:
                return self.result.caseResult('passed', f'case4093:{result}')
            else:
                return self.result.caseResult('failed', f'case4093:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4093:{e}')

    def case4094(self):
        '''
        title: 实时电流
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_current(A)'])
            self.logger.info('battery_current(A) ' + str(result))
            if result > 0:
                return self.result.caseResult('passed', f'case4094:{result}')
            else:
                return self.result.caseResult('failed', f'case4094:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4094:{e}')

    def case4095(self):
        '''
        title: 功率
        '''
        try:
            data1 = self.modbus.read_input_register_battery_status()
            result1 = float(data1['battery_voltage(V)'])
            data2 = self.modbus.read_input_register_battery_status()
            result2 = float(data2['battery_current(A)'])
            result = round(result1 * result2, 2)
            self.logger.info('battery_power(W) ' + str(result))
            if result > 0:
                return self.result.caseResult('passed', f'case4095:{result}')
            else:
                return self.result.caseResult('failed', f'case4095:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4095:{e}')

    def case4096(self):
        '''
        title: 标称容量
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_nominal_capacity(mAh)'])/1000
            self.logger.info('battery_nominal_capacity(Ah) ' + str(result))
            if result > 0:
                return self.result.caseResult('passed', f'case4096:{result}')
            else:
                return self.result.caseResult('failed', f'case4096:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4096:{e}')

    def case4097(self):
        '''
        title: 剩余容量
        '''
        try:
            data1 = self.modbus.read_input_register_battery_status()
            result1 = float(data1['battery_nominal_capacity(mAh)'])/1000
            data2 = self.modbus.read_input_register_battery_status()
            result2 = float(data2['battery_percentage_electricity'])/100
            result = round(result1 * result2, 2)
            self.logger.info('battery_remain_capacity(Ah) ' + str(result))
            if result > 0 and result <= 100:
                return self.result.caseResult('passed', f'case4097:{result}')
            else:
                return self.result.caseResult('failed', f'case4097:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4097:{e}')

    def case4098(self):
        '''
        title: 循环次数
        '''
        try:
            data = self.modbus.read_input_register_battery_status()
            result = float(data['battery_use_cycles'])
            self.logger.info('battery_use_cycles ' + str(result))
            if result > 0:
                return self.result.caseResult('passed', f'case4098:{result}')
            else:
                return self.result.caseResult('failed', f'case4098:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4098:{e}')
