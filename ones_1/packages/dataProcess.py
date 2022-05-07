#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/10 下午6:19



dataProcess = {}


class DataProcess:


    def __init__(self,taskUuid:str):
        """
        本类主要处理任务执行测试用例结果收集，以及测试结果输出
        :param taskUuid:
        """
        self.taskUuid = taskUuid

    def addTaskUuid(self):
        dataProcess[self.taskUuid] = {}

    def addCaseResult(self,taskUuid,caseUuid,caseResult):
        for key in dataProcess.keys():
            if key == taskUuid:
                dataProcess[key][caseUuid] = caseResult

    def getTaskResult(self,taskUuid):
        get = dataProcess[taskUuid]
        TOTAL = len(get) # 总用例数
        PASS,FAILED,BROKEN,SKIP = [],[],[],[] # 成功，失败。阻塞，跳过
        for key, value in get.items():
            if value == 'passed':
                PASS.append(value)
            elif value == 'failed':
                FAILED.append(value)
            elif value == 'blocked':
                BROKEN.append(value)
            else: SKIP.append(value)
        PASS = len(PASS)
        PASSRate = f'{round(PASS/TOTAL*100,2)}%'
        FAILED = len(FAILED)
        FAILEDRate = f'{round(FAILED/TOTAL*100,2)}%'
        BROKEN = len(BROKEN)
        BROKENRate = f'{round(BROKEN / TOTAL * 100, 2)}%'
        SKIP = len(SKIP)
        SKIPRate = f'{round(SKIP / TOTAL * 100, 2)}%'
        return TOTAL,PASS,PASSRate,FAILED,FAILEDRate,BROKEN,BROKENRate,SKIP,SKIPRate

    def delTaskUuid(self,taskUuid:str):
        del dataProcess[taskUuid]