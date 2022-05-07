# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase for SROS obstacle
"""

import time
import json
import unittest

import ddt
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings
from ST_test_frame.common.martix_api import Standard_Matrix_Api


@ddt.ddt
class TestObstacle(unittest.TestCase):
    '''SROS避障用例, D435参数设置。
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
        '''验证类型: 正常, 用例标题: D435参数设置, 预期结果: 参数设置成功, 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.matrix = Standard_Matrix_Api.SR_Matrix_HTTP(self.ip)
        # 配置参数
        self.matrix.modify_single_parameter(940, {'value': 'True'})
        self.matrix.modify_single_parameter(941, {'value': 'True'})
        self.matrix.modify_single_parameter(1701, {'value': 'True'})
        self.matrix.modify_single_parameter(1759, {'value': 'True'})
        time.sleep(1)
        # 读取参数
        param1 = json.loads(self.matrix.get_single_config_parameter(940))['value']
        param2 = json.loads(self.matrix.get_single_config_parameter(941))['value']
        param3 = json.loads(self.matrix.get_single_config_parameter(1701))['value']
        param4 = json.loads(self.matrix.get_single_config_parameter(1759))['value']
        self.assertEquals(set([param1, param2, param3, param4]), {'True'})


if __name__ == '__main__':
    unittest.main()
