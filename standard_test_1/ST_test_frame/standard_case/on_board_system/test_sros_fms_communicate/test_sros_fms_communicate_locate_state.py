# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-4-11
@Modify:
@Modify Date:
@Description: testcase for SROS fms communicate
"""

import unittest
import json

import ddt
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings
from ST_test_frame.common.fms_api import Standard_FMS_HTTP_API
from ST_test_frame.common.modbus_api import Standard_Modbus_Api


@ddt.ddt
class TestFmsCommunicate(unittest.TestCase):
    '''SROS小车与FMS通讯用例, 调度通信, 定位状态。
    '''

    def setUp(self) -> None:
        '''用例初始化, 开启日志模块。
        '''
        self.logger = Logs()

    def tearDown(self) -> None:
        '''用例结束处理, 清除日志模块句柄。
        '''
        self.logger.logger.handlers.pop()

    @ddt.file_data(settings.BOARD_YAML)
    def test_param_consistency(self, **kwargs):
        '''验证类型: 正常, 用例标题: 定位状态, 预期结果: 定位状态与当前定位状态保持一致, 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.base_url = kwargs['fms_url']
        self.locate_status = kwargs['locate_status']
        # 获取fms显示定位状态
        self.fms = Standard_FMS_HTTP_API.FMSApi(self.base_url)
        self.fms.login(kwargs['login']['username'], kwargs['login']['password'])
        self.fms_id = kwargs['fms_id']
        result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['location_state']
        self.logger.info('location_state: ' + result)
        self.assertIsNotNone(result)
        # 获取matrix显示定位状态
        self.modbus = Standard_Modbus_Api.SRPymodbus(self.ip)
        expect = self.modbus.read_input_register_pose_status()['positioning_status']
        self.logger.info('location_state: ' + expect)
        self.assertEqual(result, self.locate_status[expect])


if __name__ == '__main__':
    unittest.main()
