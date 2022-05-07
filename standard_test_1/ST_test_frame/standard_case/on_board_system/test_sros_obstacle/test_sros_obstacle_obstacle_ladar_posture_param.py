# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase for SROS obstacle
"""

import json
import unittest

import ddt
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings
from ST_test_frame.common.martix_api import Standard_Matrix_Api


@ddt.ddt
class TestObstacle(unittest.TestCase):
    '''SROS避障用例, 避障雷达位姿参数。
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
        '''验证类型: 正常, 用例标题: 避障雷达位姿参数, 预期结果: 与实际相符(出厂设置), 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.matrix = Standard_Matrix_Api.SR_Matrix_HTTP(self.ip)
        dict = {
            '前侧避障雷达': 2265,
            '后侧避障雷达': 2243,
            '左侧避障雷达': 2246,
            '右侧避障雷达': 2249
        }
        # 读取参数
        for i in dict:
            param1 = json.loads(self.matrix.get_single_config_parameter(dict[i]))['value']
            param2 = json.loads(self.matrix.get_single_config_parameter(dict[i] + 1))['value']
            param3 = json.loads(self.matrix.get_single_config_parameter(dict[i] + 2))['value']
            self.assertEquals([param1, param2, param3], ['0', '0', '0'])
            self.logger.info(i + 'ok')


if __name__ == '__main__':
    unittest.main()
