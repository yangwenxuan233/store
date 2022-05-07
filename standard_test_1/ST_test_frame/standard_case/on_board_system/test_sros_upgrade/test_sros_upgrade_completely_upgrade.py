# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase for SROS upgrade
"""

import time
import unittest
from pathlib import Path

import ddt
import requests
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings


@ddt.ddt
class TestUpgrade(unittest.TestCase):
    '''SROS系统固件升级用例, 固件完整包升级。
    '''

    def setUp(self) -> None:
        '''用例初始化, 开启日志模块。
        '''
        self.logger = Logs()

    def tearDown(self) -> None:
        '''用例结束处理, 清除日志模块句柄。
        '''
        self.logger.logger.handlers.pop()

    def get_system_maintenance(self):
        """获取系统维护信息,返回最新的SROS升级记录。
        """
        sros_request_url = 'http://{ip}/api/v0/upgrade_record/system'.format(ip=self.ip)  # SROS升级记录
        sros_ret = requests.get(url=sros_request_url)
        sros_upgrade_record = sros_ret.json()  # SROS升级记录，最新记录是SROS_upgrade_record[0]
        return sros_upgrade_record[0]

    @ddt.file_data(settings.BOARD_YAML)
    def test_upgrade_success(self, **kwargs):
        """验证类型: 正常, 用例标题: 固件完整包升级, 预期结果: 升级成功, 是否冒烟: 是。
        """
        self.ip = kwargs['ip']
        self.base_path = Path(settings.YAML_PATH)
        self.version_str = kwargs['version_str']
        # 获取最近更新记录
        self.last_status = self.get_system_maintenance()
        self.logger.info(self.last_status['id'])
        # 检测版本、版本修正
        if self.last_status['cur_version_str'].startswith(self.version_str):
            self.logger.info(self.last_status['cur_version_str'])
            self.firmware_name = kwargs['sros_name'][1]
            self.upgrade()
        else:
            self.logger.info(self.last_status['cur_version_str'])
        # 用例执行
        self.firmware_name = kwargs['sros_name'][0]
        self.upgrade()

    def upgrade(self):
        '''升级过程。
        '''
        self.firmware_path = list(self.base_path.glob(f"**/{self.firmware_name}"))[0]
        self.assertIsNotNone(self.firmware_path)
        self.logger.info(self.firmware_path)
        request_URL = 'http://{ip}/api/v0/update/import'.format(ip=self.ip)
        # 固件转成二进制读取
        with open(self.firmware_path, 'rb') as f:
            files = {'file': f}
            self.logger.info('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            self.assertEqual(200, ret.status_code)
            self.logger.info(ret.text)
        # 等待升级成功验证, 每隔5秒检查一次升级记录
        for i in range(40):
            time.sleep(5)
            try:
                status = self.get_system_maintenance()
                if status['finish_time'] != 0:
                    self.logger.info('升级结束')
                    break
            except Exception as e:
                self.logger.error(e)
        result = status['result']
        self.logger.info('升级结果 ' + str(result))
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
