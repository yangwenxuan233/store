import time
import unittest

import requests
from ST_test_frame.common.logs import Logs


class TestUpgrade(unittest.TestCase):
    '''SROS固件升级用例, Upgrade-01-2。
    '''

    def setUp(self) -> None:
        '''用例初始化, 开启日志。
        '''
        self.ip = '192.168.33.21'
        self.firmware_path = r'firmware_address\SROS-v4.16.0-352fc27 (2).zip'

    def tearDown(self) -> None:
        '''用例结束处理。
        '''
        return super().tearDown()

    def get_system_maintenance(self):
        """获取系统维护信息,返回最新的SROS升级记录。
        """
        try:
            SROS_request_URL = 'http://{ip}/api/v0/upgrade_record/system'.format(ip=self.ip)  # SROS升级记录
            SROS_ret = requests.get(url=SROS_request_URL)
            SROS_upgrade_record = SROS_ret.json()  # SROS升级记录，最新记录是SROS_upgrade_record[0]
            return SROS_upgrade_record[0]
        except BaseException as e:
            Logs.error('get_system_maintenance:' + str(e))

    def test_upgrade_success(self):
        """验证类型: 异常, 用例标题: 固件包格式损坏, 预期结果: 升级失败, 是否冒烟: 是。
        :param: [ip: 测试机ip地址, firmware_address: 固件包文件地址, expect: 预期结果]
        :return: None
        """
        try:
            request_URL = 'http://{ip}/api/v0/update/import'.format(ip=self.ip)
            # 固件转成二进制读取
            with open(self.firmware_path, 'rb') as f:
                files = {'file': f}
                Logs.info('正在上传文件...')
                ret = requests.post(request_URL, files=files)
            Logs.info(ret.text)
        except BaseException as e:
            Logs.error('SROS_firmware_upgrade:' + str(e))
        # 获取最近更新记录
        last_status = self.get_system_maintenance()
        # 等待升级成功验证, 每隔5秒检查一次升级记录
        for i in range(40):
            time.sleep(5)
            try:
                status = self.get_system_maintenance()
                if status['id'] > last_status['id'] and status['finish_time'] != 0:
                    Logs.info('升级结束')
                    break
            except Exception as e:
                Logs.error(e)
        result = status['result']
        Logs.info('升级结果 ' + str(result))
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()
