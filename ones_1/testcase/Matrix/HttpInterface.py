#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/11 下午5:36
# @File: HttpInterface.py


import requests
from packages.logControl import Logging
from packages.caseResult import CaseResult
from packages.yamlControl import getYamlData
from API.Matrix_API import MatrixHTTP
import json


class TestCase(object):

    def __init__(self, parameter):
        """
        本类是Matrix API对外接口测试用例
        参考：https://standard-robots.yuque.com/sn973i/dtv5kk/mg2y8d
        :param parameter:传入参数
        """
        self.result = CaseResult(parameter['task_uuid'])
        self.logger = Logging('HttpInterface')
        self.ip = parameter['AGV_IP']
        self.matrix = MatrixHTTP(self.ip)
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        self.fileDownloadPath = self.getYamlData['path']['matrix_file_download_path']

    def checkRetStatus(self, ret):
        """
        检查ret状态
        :param ret:
        :return:
        """
        try:
            if ret in range(200, 300):
                return True
            elif ret in range(400, 600):
                False
            else:
                False
        except BaseException as e:
            self.logger.error(f'checkRetStatus:{e}')

    def case4846(self):
        """
        title:使用dev账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='2')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4846:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4846:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4846:{e}')

    def case4851(self):
        """
        title:使用producer账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='producer')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4851:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4851:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4851:{e}')

    def case4857(self):
        """
        title:使用deploy账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='deploy')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4857:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4857:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4857:{e}')

    def case4858(self):
        """
        title:使用123账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='123')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4858:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4858:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4858:{e}')

    def case4853(self):
        """
        title:使用admin账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='admin')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4853:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4853:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4853:{e}')

    def case4855(self):
        """
        title:使用fms账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='fms')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4855:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4855:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4855:{e}')

    def case4854(self):
        """
        title:使用root账号登录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account='admin')
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4854:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4854:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4854:{e}')

    def case4866(self):
        """
        title:获取计划任务列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/schedule/get'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4866:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4866:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4866:{e}')

    def case4865(self):
        """
        title:获取任务模板列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission_template?id=0'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                dict_ret = ret.json()
                data = []
                for i in dict_ret:
                    del i['body']  # 去除body部分
                    data.append(i)
                return self.result.caseResult('passed', f'case4865:{data}')
            else:
                return self.result.caseResult('failed', f'case4865:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4865:{e}')

    def case4861(self):
        """
        title:获取所有用户信息
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission_template?id=0'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                dict_ret = ret.json()
                data = []
                for i in dict_ret:
                    del i['body']  # 去除body部分
                    data.append(i)
                return self.result.caseResult('passed', f'case4861:{data}')
            else:
                return self.result.caseResult('failed', f'case4861:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4861:{e}')

    def case4868(self):
        """
        title:获取系统维护信息
        :return:
        """
        try:
            SROS_request_URL = 'http://{ip}/api/v0/upgrade_record/system'.format(ip=self.ip)  # SROS升级记录
            SROS_ret = requests.get(url=SROS_request_URL, timeout=10)
            SRC_request_URL = 'http://{ip}/api/v0/upgrade_record/src'.format(ip=self.ip)  # SRC升级记录
            SRC_ret = requests.get(url=SRC_request_URL, timeout=10)
            if self.checkRetStatus(SROS_ret.status_code) == True and self.checkRetStatus(SRC_ret.status_code) == True:
                SROS_upgrade_record = SROS_ret.json()  # SROS升级记录，最新记录是SROS_upgrade_record[0]
                SRC_upgrade_record = SRC_ret.json()  # SRC升级记录，最新记录是SRC_upgrade_record[0]
                return self.result.caseResult('passed', f'case4868:{SROS_upgrade_record, SRC_upgrade_record}')
            else:
                return self.result.caseResult('failed', f'case4868:{SRC_ret.status_code},{SROS_ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4868:{e}')

    def case4867(self):
        """
        title:获取账号管理列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/accounts'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4867:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4867:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4867:{e}')

    def case4862(self):
        """
        title:获取mission任务列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/2/missions'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                dict_ret = ret.json()
                data = []
                for x in dict_ret:
                    del x['body']  # 去除body部分
                    data.append(x)
                return self.result.caseResult('passed', f'case4862:{data}')
            else:
                return self.result.caseResult('failed', f'case4862:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4862:{e}')

    def case4864(self):
        """
        title:清除mission记录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission_record/clear'.format(ip=self.ip)
            ret = requests.get(url=request_URL, timeout=10)
            if self.checkRetStatus(ret.status_code) == True:
                return self.result.caseResult('passed', f'case4864:{ret.json()}')
            else:
                return self.result.caseResult('failed', f'case4864:{ret.status_code}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4864:{e}')

    def case4870(self):
        """
        title:获取地图json文件
        :return:
        """
        try:
            self.matrix.deleteMap('SRTOS测试') # 先删除地图
            fileRet = self.matrix.mapFileFMSImport('./testcase/Matrix/dependenciesFile/SRTOS测试_nav.map_export') # 导入测试地图
            ret = self.checkRetStatus(fileRet)
            map_name = 'SRTOS测试'
            if ret == True:
                request_URL = 'http://{ip}/api/v0/map/{map_name}/data'.format(ip=self.ip, map_name=map_name)
                ret = requests.get(url=request_URL, stream=True)
                ret_json = json.dumps(ret.json(), ensure_ascii=False, indent=1, sort_keys=False)  # 格式转成json字符串
                with open('{}{}.json'.format(self.fileDownloadPath, map_name), 'w') as code:
                    code.write(ret_json)
                self.logger.info('{}.json download complete'.format(map_name))
                self.matrix.deleteMap('SRTOS测试')  # 删除地图
                return self.result.caseResult('passed', f'case4870:jsonFile：{map_name}', isUpload=True,
                                              attachments_address='/home/weisen/ONES_AutoTest/download/Matrix/SRTOS测试.json',
                                              fileName='SRTOS测试.json', description='已成功下载的json文件')
            else:
                return self.result.caseResult('failed', f'case4870:{ret}')
        except BaseException as e:
            return self.result.caseResult('failed', f'case4870:{e}')