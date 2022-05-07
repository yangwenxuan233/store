#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ywx
# @Modify: add testcases
# @Time: 2022/4/21 15:30


import json

from API.FMS_API import FMSApi
from API.Matrix_API import MatrixHTTP
from API.Modbus_Api import SR_Pymodbus
from packages.caseResult import CaseResult
from packages.logControl import Logging
from packages.yamlControl import getYamlData


class TestCase:

    def __init__(self, parameter):
        self.parameter = parameter
        self.logger = Logging('fmsCommunicate')
        self.matrix = MatrixHTTP(self.parameter['AGV_IP'])
        self.result = CaseResult(parameter['task_uuid'])
        self.ip = self.parameter['AGV_IP']
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        self.base_url = self.getYamlData['fms_url']
        self.fms = FMSApi(self.base_url)
        self.modbus = SR_Pymodbus(self.ip)
        self.locate_status = self.getYamlData['locate_status']
        self.move_status = self.getYamlData['move_status']
        self.system_status = self.getYamlData['system_status']
        self.fms_id = self.parameter['id']

    def case4223(self):
        '''
        title: sros版本号
        '''
        try:
            # 获取fms显示sros版本号
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['sros_version'][: 15]
            self.logger.info('fms_sros_version: ' + result)
            # 获取matrix显示sros版本号
            expect = self.matrix.getSystemMaintenance()[0]['cur_version_str'][: 15]
            self.logger.info('matrix_sros_version: ' + expect)
            if expect == result:
                self.result.caseResult('passed', f'case4223:{result}')
            else:
                self.result.caseResult('failed', f'case4223:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4223:{e}')

    def case4224(self):
        '''
        title: src版本号
        '''
        try:
            # 获取fms显示src版本号
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['src_version'][: 15]
            self.logger.info('fms_src_version: ' + result)
            # 获取matrix显示src版本号
            expect = self.matrix.getSystemMaintenance()[1]['cur_version_str'][: 15]
            self.logger.info('matrix_src_version: ' + expect)
            if expect == result:
                self.result.caseResult('passed', f'case4224:{result}')
            else:
                self.result.caseResult('failed', f'case4224:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4224:{e}')

    def case4225(self):
        '''
        title: 定位状态
        '''
        try:
            # 获取fms显示定位状态
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['location_state']
            self.logger.info('location_state: ' + result)
            # 获取matrix显示定位状态
            expect = self.modbus.read_input_register_pose_status()['positioning_status']
            self.logger.info('positioning_state: ' + expect)
            if result == self.locate_status[expect]:
                self.result.caseResult('passed', f'case4225:{result}, {expect}')
            else:
                self.result.caseResult('failed', f'case4225:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4225:{e}')

    def case4226(self):
        '''
        title: 运动状态
        '''
        try:
            # 获取fms显示运动状态
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['move_state']
            self.logger.info('move_state: ' + result)
            # 获取matrix显示运动状态
            expect = self.modbus.read_input_register_pose_status()['move_task_status']
            self.logger.info('move_task_status: ' + expect)
            if result == self.move_status[expect]:
                self.result.caseResult('passed', f'case4226:{result}, {expect}')
            else:
                self.result.caseResult('failed', f'case4226:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4226:{e}')

    def case4227(self):
        '''
        title: 载货状态
        '''
        try:
            # 获取fms显示运动状态
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['load_state']
            self.logger.info('load_state: ' + result)
            expect = 0
            if result == expect:
                self.result.caseResult('passed', f'case4227:{result}, {expect}')
            else:
                self.result.caseResult('failed', f'case4227:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4227:{e}')

    def case4228(self):
        '''
        title: 系统状态
        '''
        try:
            # 获取fms显示运动状态
            result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['system_state']
            self.logger.info('system_state: ' + result)
            # 获取matrix显示运动状态
            expect = self.modbus.read_input_register_pose_status()['system_status']
            self.logger.info('system_status: ' + expect)
            if result == self.system_status[expect]:
                self.result.caseResult('passed', f'case4228:{result}, {expect}')
            else:
                self.result.caseResult('failed', f'case4228:{result}, {expect}')
        except Exception as e:
            return self.result.caseResult('failed', f'case4228:{e}')
