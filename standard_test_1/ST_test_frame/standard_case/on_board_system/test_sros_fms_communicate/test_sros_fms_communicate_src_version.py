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
from ST_test_frame.common.martix_api import Standard_Matrix_Api


@ddt.ddt
class TestFmsCommunicate(unittest.TestCase):
    '''SROS小车与FMS通讯用例, 调度通信, src版本号。
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
        '''验证类型: 正常, 用例标题: src版本号, 预期结果: src版本号与Matrix显示一致, 是否冒烟: 否。
        '''
        self.ip = kwargs['ip']
        self.base_url = kwargs['fms_url']
        # 获取fms显示src版本号
        self.fms = Standard_FMS_HTTP_API.FMSApi(self.base_url)
        self.fms.login(kwargs['login']['username'], kwargs['login']['password'])
        self.fms_id = kwargs['fms_id']
        result = json.loads(self.fms.get_specific_vehicle(self.fms_id))['src_version'][: 15]
        self.assertIsNotNone(result)
        self.logger.info('fms_src_version: ' + result)
        # 获取matrix显示src版本号
        self.matrix = Standard_Matrix_Api.SR_Matrix_HTTP(self.ip)
        expect = self.matrix.get_system_maintenance()[1]['cur_version_str'][: 15]
        self.assertIsNotNone(expect)
        self.logger.info('matrix_src_version: ' + expect)
        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()
