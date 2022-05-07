#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ywx
# @Modify: add testcases
# @Time: 2022/4/20 11:11


import threading
import time

import requests
from API.Matrix_API import MatrixHTTP
from packages.caseResult import CaseResult
from packages.logControl import Logging
from packages.yamlControl import getYamlData


class TestCase:

    def __init__(self, parameter):
        self.parameter = parameter
        self.logger = Logging('firmwareUpgrade')
        self.matrix = MatrixHTTP(self.parameter['AGV_IP'])
        self.result = CaseResult(parameter['task_uuid'])
        self.ip = self.parameter['AGV_IP']
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        self.base_path = self.getYamlData['path']['ones_file_download_path']

    def upgrade(self):
        '''升级过程。
        '''
        self.logger.info(self.firmware_path)
        request_URL = 'http://{ip}/api/v0/update/import'.format(ip=self.ip)
        # 固件转成二进制读取
        with open(self.firmware_path, 'rb') as f:
            files = {'file': f}
            self.logger.info('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            self.logger.info(ret.text)
        # 等待升级成功验证, 每隔5秒检查一次升级记录
        for i in range(40):
            time.sleep(5)
            try:
                status = self.matrix.getSystemMaintenance()[0]
                if status['finish_time'] != 0 and status['id'] > self.last_status['id']:
                    self.logger.info('升级结束')
                    break
            except Exception as e:
                self.logger.error(e)
        self.logger.info('升级结果 ' + str(status['result']))
        return status

    def upload_file(self):
        '''上传固件包。(post)
        '''
        request_URL = 'http://{ip}/api/v0/update/import'.format(ip=self.ip)
        with open(self.firmware_path, 'rb') as f:
            files = {'file': f}
            self.logger.info('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            self.logger.info(ret.text)

    def case3933(self):
        """
        title: 固件完整包升级
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            result = self.upgrade()
            if result['result'] == 1:
                return self.result.caseResult('passed', f'case3933:{result}')
            else:
                return self.result.caseResult('failed', f'case3933:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3933:{e}')

    def case3935(self):
        """
        title: 固件包大小异常升级
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            result = self.upgrade()
            if result['result'] == 0:
                return self.result.caseResult('passed', f'case3935:{result}')
            else:
                return self.result.caseResult('failed', f'case3935:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3935:{e}')

    def case3938(self):
        """
        title: 固件包上传过程中断网
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            #  开启上传文件线程，1秒后中断
            th = threading.Thread(target=self.upload_file)
            th.start()
            time.sleep(1)
            th.join()
            # 等待升级成功验证, 每隔5秒检查一次升级记录
            for i in range(12):
                time.sleep(5)
                try:
                    status = self.matrix.getSystemMaintenance()[0]
                    if status['finish_time'] != 0 and status['id'] > self.last_status['id']:
                        self.logger.info('升级结束')
                        result = 1
                        break
                    else:
                        result = 0
                except Exception as e:
                    self.logger.error(e)
            self.logger.info('升级结果 ' + str(result))
            if result['result'] == 0:
                return self.result.caseResult('passed', f'case3938:{result}')
            else:
                return self.result.caseResult('failed', f'case3938:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3938:{e}')

    def case3936(self):
        """
        title: 不同版本固件包升级
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            result = self.upgrade()
            if result['result'] == 1:
                return self.result.caseResult('passed', f'case3936:{result}')
            else:
                return self.result.caseResult('failed', f'case3936:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3936:{e}')

    def case3940(self):
        """
        title: 固件包重命名后升级
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            result = self.upgrade()
            if result['result'] == 1:
                return self.result.caseResult('passed', f'case3940:{result}')
            else:
                return self.result.caseResult('failed', f'case3940:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3940:{e}')

    def case3941(self):
        """
        title: 回退旧版本SROS固件
        """
        try:
            self.firmware_name = self.parameter['taskAttachmentsInfo']
            self.firmware_path = self.base_path + self.firmware_name
            self.last_status = self.matrix.getSystemMaintenance()[0]
            self.logger.info(self.last_status['id'])
            result = self.upgrade()
            if result['result'] == 1:
                return self.result.caseResult('passed', f'case3941:{result}')
            else:
                return self.result.caseResult('failed', f'case3941:{result}')
        except Exception as e:
            return self.result.caseResult('failed', f'case3941:{e}')
