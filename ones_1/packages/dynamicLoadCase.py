#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/12 上午9:15




import re,json,os
from packages.yamlControl import getYamlData
from packages.logControl import Logging





class LoadCaseDriver:

    def __init__(self):
        """
        本类主要功能检索testcase目录下用例驱动，并将用例驱动自动更新到testCaseDrive.json
        """
        self.logger = Logging('LoadingCaseDriver')
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        self.testCaseDrivePath = self.getYamlData['path']['case_drive_path']  # 用例驱动地址

    def loadCaseDrive(self) -> dict:
        """
        加载测试用例驱动
        :return:
        """
        try:
            file = open(self.testCaseDrivePath + 'testCaseDrive.json', "rb")
            fileJson = json.load(file)
            return fileJson
        except BaseException as e:
            self.logger.error('loadCaseDrive:' + str(e))

    def updateCaseDrive(self,caseId:str,caseInfo:dict):
        """
        更新用例驱动
        :return:
        """
        try:
            caseDict = self.loadCaseDrive()
            caseDict[caseId] = caseInfo
            with open(self.testCaseDrivePath + 'testCaseDrive.json', "w",encoding='utf-8') as f:
                f.write(json.dumps(caseDict,ensure_ascii=False, indent=2, sort_keys=False))
                f.close()
        except BaseException as e:
            self.logger.error(f'updateCaseDrive:{e}')

    def delCaseDrive(self,caseId:str):
        """
        删除用例驱动
        :param caseId:
        :return:
        """
        try:
            caseDict = self.loadCaseDrive()
            del caseDict[caseId]
            with open(self.testCaseDrivePath + 'testCaseDrive.json', "w", encoding='utf-8') as f:
                f.write(json.dumps(caseDict, ensure_ascii=False, indent=2, sort_keys=False))
                f.close()
        except BaseException as e:
            self.logger.error(f'delCaseDrive:{e}')

    def findAllFile(self,filePath:str):
        for root, ds, fs in os.walk(filePath):
            for f in fs:
                fullname = os.path.join(root, f)
                yield fullname

    def dynamicImportCaseDrive(self, path):
        """
        动态导入用例驱动
        :param path, path = './testcase/'
        :return:
        """
        for filePath in self.findAllFile(path):
            if '.pyc' not in filePath and '__init__.py' not in filePath:
                if '.py' in filePath:
                    checkId = [] # 将py文件的caseId收集，用来去除不存在的caseId
                    caseFilePath = filePath[2:]
                    caseDriveIdList = list(self.loadCaseDrive().keys())
                    with open(filePath,'r', encoding='UTF-8') as f:
                        for line in f:
                            if "    def case" in line:
                                caseId = re.findall("\d+", line)[0]
                                if caseId not in caseDriveIdList:
                                    checkId.append(caseId)
                                    self.updateCaseDrive(caseId,{"file_address":caseFilePath,'title':''})
                                else:
                                    checkId.append(caseId)
                            elif 'title' in line:
                                title = line.replace('\n','').replace('        ','')
                                self.updateCaseDrive(caseId,{"file_address":caseFilePath,'title':title[6:]})
                            else:
                                pass
                    # 删除不存在的caseId
                    if checkId != []:
                        for id in caseDriveIdList:
                            if id not in checkId:
                                self.delCaseDrive(id)