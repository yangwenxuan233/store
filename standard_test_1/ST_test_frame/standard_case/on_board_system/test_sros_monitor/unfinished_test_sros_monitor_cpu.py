# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase for SROS monitor
"""

# import json
import unittest

import ddt
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings
from ST_test_frame.common.modbus_api import Standard_Modbus_Api


@ddt.ddt
class TestObstacle(unittest.TestCase):
    '''SROS避状态监控用例, 性能状态监控, cpu使用率。
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
    def test_set_param_succeful(self, **kwargs):
        '''验证类型: 正常, 用例标题: cpu使用率, 预期结果: 状态能正确显示, 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.modbus = Standard_Modbus_Api.SRPymodbus(self.ip)
        data = self.modbus.read_discrete_inputs_all_status()
        print(data)


if __name__ == '__main__':
    unittest.main()
