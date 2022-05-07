# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase for SROS monitor
"""

import unittest

import ddt
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings
from ST_test_frame.common.modbus_api import Standard_Modbus_Api


@ddt.ddt
class TestObstacle(unittest.TestCase):
    '''SROS状态监控用例, 电池监控, 电池功率。
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
    def test_param_allright(self, **kwargs):
        '''验证类型: 正常, 用例标题: 电池功率, 预期结果: 功率状态正常, 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.modbus = Standard_Modbus_Api.SRPymodbus(self.ip)
        data1 = float(self.modbus.read_input_register_battery_status()['battery_voltage(V)'])
        data2 = float(self.modbus.read_input_register_battery_status()['battery_current(A)'])
        data = round(data1 * data2, 2)
        self.logger.info('battery_power(W) ' + str(data))
        self.assertTrue(data > 0)


if __name__ == '__main__':
    unittest.main()
