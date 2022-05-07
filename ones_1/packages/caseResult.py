#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/7 下午10:27



class CaseResult:
    """
    测试用例执行结果回填
    """
    def __init__(self,taskUuid):
        self.taskUuid = taskUuid

    def caseResult(self,result,note,isUpload=False,attachments_address='',fileName='',description=''):
        """
        用例执行结果
        :param result: 用例结果 '通过': 'passed',’失败': 'failed','阻塞': 'blocked''跳过': 'skipped'
        :param note: 测试备注
        :param isUpload: 是否上传附件，默认False
        :param attachments_address: 附件地址
        :param fileName: 上传文件名
        :param description: 文件备注信息
        :return:
        """
        caseResult = {
            "resultInfo": {
                "cases": [{
                    "uuid": None,  # 测试用例uuid
                    "executor": None,  # 执行者 uuid
                    "note": result,  # 执行结果备注
                    "result": result,  # 测试结果
                    "steps": [{  # 执行步骤
                        "uuid": None,  # 执行步骤uuid
                        "actual_result": note,  # 实际结果备注
                        "execute_result": result  # 执行步骤结果
                    }]
                }],
                "is_batch": False  # 是否批量
            },  # 测试结果信息
            "upload attachments":{
                "is upload": isUpload,  # 是否上传附件
                "attachments address": attachments_address,  # 上传附件地址
                "fileName": fileName,
                "description":description # 对文件的备注
            },
            "caseResult": result, # 用例执行结果用来汇总执行情况
            'task_uuid': self.taskUuid # 任务uuid
        }
        return caseResult