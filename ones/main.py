#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/3/30 下午11:27


import json
from API.ONES_API import OnesAPI
from packages.logControl import Logging
import time
from packages.yamlControl import getYamlData
from packages.ThreadPoolExecutor import ThreadPool
import os
import importlib
from operator import methodcaller
from testcase.Init_robot import Init_Robot
from packages.dataProcess import DataProcess
from packages.dingtalk import DingTalk
from packages.dynamicLoadCase import LoadCaseDriver


class LazyImport:
    """
    动态导入模块
    """

    def __init__(self, module_name, module_class):
        """
        等同于 form module_name import module_class
        :param module_name:
        :param module_class:
        :return:
        """
        self.module_name = module_name
        self.module_class = module_class
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, fromlist=[self.module_class])
        return getattr(self.module, name)


class TaskManager:

    def __init__(self):
        """
        本类为任务管理器，主要处理ONES Project任务下发，到用例执行以及结果回填等事务
        """
        self.version = 'V1.0.1'  # 版本号
        self.logger = Logging('TaskManager')
        self.startRecording()  # 开始记录日志
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        # ONES API账号与密码
        self.ONES_email = self.getYamlData['ones_api']['ones_email']
        self.ONES_password = self.getYamlData['ones_api']['ones_passwd']
        self.ONES_API = OnesAPI(self.ONES_email, self.ONES_password)  # ONES API接口初始化
        self.testCaseDrivePath = self.getYamlData['path']['case_drive_path']  # 用例驱动地址
        self.dynamicCaseDrive = LoadCaseDriver()  # 加载自动更新用例驱动
        self.dingtalk = DingTalk()  # 钉钉机器人通知初始化
        self.taskQueue = []  # 任务队列
        self.testPlan = None
        self.task = None  # 任务状态标记位
        self.event = True  # 停止查询任务状态，默认True
        self.agv_ip = []  # 测试车辆队列
        self.threadPool = ThreadPool(10)  # 启用线程池管理器
        self.checkFolder()  # 检查所用的文件夹是否被创建

    def queryTaskStatus(self):
        """
        查询任务状态
        :return:
        """
        try:
            while self.event != False:
                time.sleep(1)  # 每1秒查询一次
                taskInfoList = self.ONES_API.get_ProjectTask_items()  # 返回进行中的任务列表
                if taskInfoList == []:  # 无处于进行中的任务
                    pass
                else:
                    for taskInfo in taskInfoList:
                        task_uuid = taskInfo['task_uuid']
                        parameter = self.ONES_API.getProjectTaskTransitions(task_uuid)
                        if parameter['related_testcase_plans'] == '' \
                                or parameter['AGV_IP'] == "":
                            self.logger.info(
                                f'Task:{taskInfo["task_name"]} Detection not associated with test plan or AGV_IP...')
                            self.ONES_API.update_ProjectTask_Status(task_uuid, '已完成')  # 任务状态修改成已完成
                            self.updateNotesAndProgress(task_uuid, '无关联测试计划，任务结束', 100)
                        else:
                            if self.task == None or self.task != task_uuid and task_uuid not in self.taskQueue:
                                relatedTestPlans = parameter['related_testcase_plans']  # 关联测试计划
                                if task_uuid not in self.taskQueue:
                                    self.testPlan = relatedTestPlans
                                    parameter['task_uuid'] = task_uuid  # 往参数添加task_uuid
                                    AGV_IP = parameter['AGV_IP']
                                    if self.initRobot(AGV_IP) == True and AGV_IP not in self.agv_ip:
                                        # 满足条件的任务AGV_IP不相同时
                                        self.dynamicCaseDrive.dynamicImportCaseDrive('./testcase/')  # 动态加载用例驱动
                                        self.threadPool.run(self.runTestPlan, parameter)  # 将任务加入线程池运行
                                        self.task = task_uuid
                                        self.agv_ip.append(AGV_IP)
                                        self.taskQueue.append(task_uuid)  # 往队列添加任务
                                    else:
                                        self.ONES_API.update_ProjectTask_Status(task_uuid, '已完成')  # 任务状态修改成已完成
                                        self.updateNotesAndProgress(task_uuid,
                                                                    '初始化AGV失败，请检查AGV是否正常或者使用正在运行车辆IP...',
                                                                    100)
                                        self.logger.info('Task：{}，Init_robot fail!'.format(task_uuid))
        except BaseException as e:
            self.logger.error('queryTaskStatus:' + str(e))

    def runTestPlan(self, parameter):
        """
        运行测试计划,多任务情况下，每个线程运行一个任务
        :param parameter: 测试计划相关信息
        :return:
        """
        try:
            task_uuid = parameter['task_uuid']
            testPlan = parameter['related_testcase_plans'] # 测试计划名称
            self.logger.info('Received task:{},task processing...'.format(task_uuid))
            self.updateNotesAndProgress(task_uuid, "任务已受理，正在执行测试计划中的自动化用例，请关注钉钉群通知...", 10)
            # self.dingtalk.sendStartTask(parameter['type'],parameter['summary'],parameter['assign']) # 任务受理钉钉通知
            testCaseList = self.ONES_API.getTestCaseListName(testPlan)  # 获取所有测试用例
            taskAttachmentsInfo = self.downloadTaskAttachments(task_uuid)  # 下载任务附件文件
            if taskAttachmentsInfo != None:  # 添加附件信息到parameter
                parameter['taskAttachmentsInfo'] = taskAttachmentsInfo
            caseDriveIdList = list(self.loadCaseDrive().keys())  # 加载用例驱动列表
            self.logger.info(f'Get the test plan:{testPlan} total number of test cases：{len(testCaseList)}')
            self.ONES_API.update_testplan_status('进行中', testPlan)
            dataProcess = DataProcess(task_uuid)
            dataProcess.addTaskUuid()
            parameter['testPlanUuid'] = self.ONES_API.getTestPlanInfo(testPlan)['uuid']  # 添加testPlanUuid
            parameter['time_stamp'] = self.nowToTimestamp()  # 添加开始执行测试时间戳
            try:
                repeatNumber = int(parameter['repeatNumber'])  # 用例重复运行次数
            except BaseException:
                repeatNumber = 1
            num = 0
            while num < repeatNumber:  # 添加任务重复次数功能
                num += 1
                for testcase in testCaseList:
                    caseId = testcase['number']
                    if str(caseId) in caseDriveIdList:
                        # 获取case相关uuid信息
                        caseInfo = self.ONES_API.getTestCaseInfo(int(testcase['number']), testPlan)
                        caseUuid = caseInfo['cases'][0]['uuid']
                        executorUuid = testcase['executor']
                        stepsUuid = caseInfo['cases'][0]['steps'][0]['uuid']
                        dir = self.loadCaseDrive().get(str(caseId))['file_address']
                        dynamic = self.dynamic_import(dir)  # 动态导入模块
                        case = dynamic.TestCase(parameter)  # 测试用例的py文件的类必须是TestCase
                        caller = methodcaller(f"case{caseId}")  # 通过methodCaller运行指定测试用例
                        result = caller(case)  # 测试用例执行完成后接收结果
                        if result != None:  # 去除没有用例驱动情况
                            self.threadPool.acquire()  # 添加线程锁
                            caseUuid, caseResult = self.processCaseResult(result, testPlan, caseUuid, executorUuid,
                                                                          stepsUuid)
                            self.logger.info(
                                f"updateTestCaseStatus:['caseName':{testcase['name']},'caseUuid':{caseUuid},'caseResult':{result['caseResult']}]")
                            dataProcess.addCaseResult(task_uuid, caseUuid, caseResult)
                        del dynamic, case, caller, result
            reportUuid = self.addTestReport(testPlan,parameter['testPlanUuid'],parameter['time_stamp'])
            reportShareLink = self.ONES_API.reportShareLink(parameter['testPlanUuid'], reportUuid) # 获取测试报告链接
            self.ONES_API.update_ProjectTask_Status(task_uuid, '已完成')  # 任务状态修改成已完成
            self.updateNotesAndProgress(task_uuid, "测试计划中的自动化测试用例已执行完成，任务结束", 100)
            TOTAL, PASS, PASSRate, FAILED, FAILEDRate, BROKEN, BROKENRate, SKIP, SKIPRate = dataProcess.getTaskResult(task_uuid)
            self.dingtalk.sendNotification(parameter['type'],
                                           parameter['summary'],
                                           parameter['assign'],
                                           TOTAL,
                                           PASS,
                                           PASSRate,
                                           FAILED,
                                           FAILEDRate,
                                           BROKEN,
                                           BROKENRate,
                                           SKIP,
                                           SKIPRate,
                                           reportShareLink)
            dataProcess.delTaskUuid(task_uuid)
            self.logger.info(f'Task：{task_uuid}，The automation use case in the test plan has been executed')
            self.task = None
            self.taskQueue.remove(task_uuid)  # 完成任务后从队列清除
            self.agv_ip.remove(parameter['AGV_IP'])  # 完成任务后从IP队列清除
            del task_uuid, TOTAL, PASS, PASSRate, FAILED, FAILEDRate, BROKEN, BROKENRate, SKIP, SKIPRate, reportShareLink, reportUuid
        except BaseException as e:
            self.logger.error('runTestPlan: ' + str(e))

    def processCaseResult(self, result: dict, testPlan: str, caseUuid: str, executorUuid: str, stepsUuid: str):
        """
        处理测试用例返回的结果
        :param result: 用例执行结果
        :param testPlan: 测试计划
        :param caseUuid: 用例uuid
        :param executorUuid: 执行人uuid
        :param stepsUuid: 执行步骤uuid
        :return:
        """
        try:
            caseResultInfo, caseResult, uploadInfo = result['resultInfo'], result['caseResult'], result[
                'upload attachments']
            if uploadInfo['is upload'] == True:
                # 上传附件到测试用例
                self.ONES_API.uploadAttachmentToCase(uploadInfo['attachments address'], caseUuid,
                                                     uploadInfo['fileName'], uploadInfo['description'])
            # 更新测试用例信息
            self.updateCaseStatus(caseResultInfo, testPlan, caseUuid, executorUuid, stepsUuid)
            self.threadPool.release()  # 解除线程锁
            return caseUuid, caseResult
        except BaseException as e:
            self.logger.error('processCaseResult:' + str(e))

    def addTestReport(self,testPlanName:str,testPlanUuid:str,start_time=0):
        """
        获取测试计划是否已生成测试报告,若测试计划已有测试报告则取第一个报告uuid
        :param testPlanName: 测试计划名称
        :param testPlanUuid: 测试计划uuid
        :param start_time: 开始时间
        :return:
        """
        try:
            # 获取测试计划里是否已生成测试报告
            planReportsInfo = self.ONES_API.getTestPlanDetails(testPlanName)['data']['testcasePlans'][0]['planReports']
            if planReportsInfo == []:
                reportUuid = self.ONES_API.addTestReport(testPlanUuid,
                                                         self.reportName(),
                                                         start_time)
                return reportUuid
            else:
                reportUuid = planReportsInfo[0]['uuid']
                self.ONES_API.updateReport(self.reportName(),reportUuid,start_time)
                return reportUuid # 返回第一个测试报告uuid
        except BaseException as e:
            self.logger.error(f'getTestPlanReportInfo:{e}')

    def reportName(self):
        """
        输出测试报告名称
        :return:
        """
        try:
            current_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
            return f'{current_time} TestReport'
        except BaseException as e:
            self.logger.error(f'reportName:{e}')

    def nowToTimestamp(self, digits=10):
        """
        获取当前时间搓
        :param digits:
        :return:
        """
        time_stamp = time.time()
        digits = 10 ** (digits - 10)
        time_stamp = int(round(time_stamp * digits))
        return time_stamp

    def startRecording(self):
        """
        开始记录日志
        :return:
        """
        try:
            info = "Start RunService！Version:{}\r".format(self.version)
            self.logger.info(info)
        except BaseException as e:
            self.logger.error('start_recording: ' + str(e))

    def checkFolder(self):
        """
        检查config.yaml文件里的path地址文件夹是否创建，若没有则创建
        :return:
        """
        try:
            getPath = self.getYamlData['path']
            for path in getPath:
                if not os.path.exists(getPath[path]):
                    os.makedirs(getPath[path])
        except BaseException as e:
            self.logger.error('checkFolder:' + str(e))

    def module_name(self, module_name: str):
        """
        :param module_name:
        :return:
        """
        original = module_name.replace('/', '.')
        return original[:original.rfind('.')]

    def dynamic_import(self, module_name: str):
        """
        动态导入模块
        :param module_name:
        :return:
        """
        module = importlib.import_module(self.module_name(module_name))
        return module

    def loadCase(self, path) -> list:
        """
        加载测试用例
        :param path: 测试用例地址
        :return:
        """
        dirlist = os.listdir(path)
        return dirlist

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

    def downloadTaskAttachments(self, taskUuid: str):
        """
        下载任务附件资源
        :param taskUuid: 任务uuid
        :return:
        """
        try:
            attachmentsINFO = self.ONES_API.getProjectTaskAttachments(taskUuid)
            if attachmentsINFO['count'] != 0:
                for info in attachmentsINFO['attachments']:
                    if info['status'] == 1:  # 1为资源可用，2为资源不可用
                        self.logger.info('Downloading {}...'.format(info['name']))
                        self.ONES_API.downloadTaskAttachments(taskUuid, info['name'])
                        return info['name']
        except BaseException as e:
            self.logger.error('downloadTaskAttachments:' + str(e))

    def updateCaseStatus(self, caseResult: dict, testPlan: str, caseUuid: str, executorUuid: str, stepsUuid: str):
        """
        更新测试用例状态
        :param caseResult: 用例执行结果
        :param testPlan: 测试计划名称
        :param caseUuid: 测试用例UUID
        :param executorUuid: 执行人uuid
        :param stepsUuid: 步骤uuid
        :return:
        """
        try:
            # 替换原来None的值
            caseResult['cases'][0]['uuid'] = caseUuid
            caseResult['cases'][0]['executor'] = executorUuid
            caseResult['cases'][0]['steps'][0]['uuid'] = stepsUuid
            return self.ONES_API.updateTestCaseStatus(caseResult, testPlan)
        except BaseException as e:
            self.logger.error('updateCaseStatus:' + str(e))

    def updateProjectTaskNotes(self, task_uuid: str, note: str):
        """
        添加任务备注信息
        :param task_uuid: 任务uuid
        :param note:备注信息
        :return:
        """
        try:
            self.ONES_API.update_ProjectTask_field_values(task_uuid,
                                                          {"field_uuid": "EURcRZ3M", "type": 15, "value": note})
        except BaseException as e:
            self.logger.error('updateProjectTaskNotes:' + str(e))

    def modifyProgress(self, task_uuid: str, value: int):
        """
        修改执行进度
        :param task_uuid: 任务uuid
        :param value: 执行进度:0-100
        :return:
        """
        try:
            self.ONES_API.update_ProjectTask_field_values(task_uuid, {"field_uuid": "Nj2xP8YJ", "type": 3,
                                                                      "value": value * 100000})  # 执行进度修改100
        except BaseException as e:
            self.logger.error('updateProjectTaskNotes:' + str(e))

    def updateNotesAndProgress(self, task_uuid: str, note: str, value: int):
        try:
            self.updateProjectTaskNotes(task_uuid, note)
            self.modifyProgress(task_uuid, value)
        except BaseException as e:
            self.logger.error(f'updateNotesAndProgress:{e}')

    def initRobot(self, AGV_IP: str) -> bool:
        """
        初始化测试车辆
        :param AGV_IP:
        :return:
        """
        try:
            self.logger.info('robot:{} initializing...'.format(AGV_IP))
            initRobot = Init_Robot(AGV_IP)
            ret = initRobot.init_robot()
            return True
            # if ret == 'Init robot successful':
            #     return True
            # else:
            #     return False
        except BaseException as e:
            self.logger.error('initRobot:' + str(e))

    def stopQueryTaskStatus(self):
        """
        停止运行查询服务,停止相关的服务
        :return:
        """
        try:
            self.event = False
            time.sleep(1)  # 等待开启线程停止
            self.ONES_API.signOut()
            self.threadPool.terminate()
        except BaseException as e:
            self.logger.error('stopQueryTaskStatus:' + str(e))