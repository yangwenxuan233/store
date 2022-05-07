#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/24 下午1:54
# @File: test.py
#
# from API.ONES_API import OnesAPI
#
# if __name__ == '__main__':
#
#     test = OnesAPI('weisen@standard-robots.com','13876603223as')
#     # print(test.addTestReport('THi5zUxY','weisen')) # RFV52oNk
#     # test.updateReport('测试报告','RFV52oNk')
#     print(test.getTestPlanInfo('测试'))

import time
from testcase.Modbus.modbusInterface import TestCase


if __name__ == '__main__':
    parameter = {
                "summary": "",
                "task_uuid": "",
                'assign': "",  # 任务负责人
                "testPlan": "",
                'AGV_IP': "192.168.33.123",
                'Device_IP': ""
            }

    test = TestCase(parameter)
    for i in dir(TestCase):
        if i.startswith('case'):
            print(i)
            data = getattr(test, i)()
            print(data['caseResult'])
            print('----------------------------')
            time.sleep(3)
