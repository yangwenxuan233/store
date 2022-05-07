# -*- coding:utf-8 -*-
# Standard_ONES_API
# Author: weisen
# time:20210925
import time

import requests
import json
from packages.logControl import Logging
from packages.yamlControl import getYamlData



class OnesAPI:

    def __init__(self, email: str, password: str):
        """
        本类主要是ONES API，主要功能实现对测试计划调用、读取测试计划中的测试用例并修改测试用例状态等
        :param email: 邮箱账号
        :param password: 密码
        :return:
        """
        self.logger = Logging('ONES_API')
        self.getYamlData = getYamlData()  # 加载config.yaml文件
        self.fileDownloadPath = self.getYamlData['path']['ones_file_download_path']
        self.user_token = None  # 用户token
        self.user_uuid = None  # 用户id
        self.teams_uuid = None  # 团队id
        self.login(email, password)

    def login(self, email: str, password: str):
        """
        ONES账号登录接口
        :param email: 邮箱账号
        :param password: 密码
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/auth/login'
            json_request = {
                'email': email,
                'password': password
            }
            ret = requests.post(url=request_URL, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            self.user_token = ret.json()['user']['token']  # 获取token
            self.user_uuid = ret.json()['user']['uuid']  # 获取用户id
            self.teams_uuid = ret.json()['teams'][0]['uuid']  # 获取用户在团队id
            self.logger.info('login success!')
            return json_ret
        except BaseException as e:
            self.logger.error('login fail:' + str(e))

    def getTeamsInfo(self)->dict:
        """
        获取团队信息，返回json信息
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teams_uuid}/info'.format(
                teams_uuid=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            return ret.json()
        except BaseException as e:
            self.logger.error('get_teams_info : ' + str(e))

    def signOut(self):
        """
        退出ONES登录,返回http_status_code=200或者null
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/auth/logout'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            self.logger.info('sign out!')
            return ret.text
        except BaseException as e:
            self.logger.error('sign_out:' + str(e))

    def get_userProject_list(self):
        """
        获取当前用户Project列表信息
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teams_uuid}/projects/my_project'.format(
                teams_uuid=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            self.logger.error('get_userProject_list:' + str(e))

    def get_userProjectUUID(self, Project: str):
        """
        获取项目的uuid信息
        :param Project:
        :return:
        """
        try:
            userProject_list = json.loads(self.get_userProject_list())['projects']
            for i in userProject_list:
                if i['name'] == Project:
                    userProjectUUID = i['uuid']
                    return userProjectUUID
            return '没有找到相关项目！'
        except BaseException as e:
            self.logger.error('get_userProjectUUID:' + str(e))

    def get_userProject_iteration_list(self, project_name: str):
        """
        获取当前项目下的迭代信息；project_name：项目名称
        :param project_name:
        :return:
        """
        try:
            project_list = json.loads(self.get_userProject_list())['projects']
            for i in project_list:
                if i['name'] == project_name:
                    project_uuid = i['uuid']  # 获取项目的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teams_uuid}/project/{projectUUID}/sprints'.format(
                        teams_uuid=self.teams_uuid, projectUUID=project_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
                    return json_ret
        except BaseException as e:
            self.logger.error('get_userProject_iteration_list:' + str(e))

    def get_userProject_iterationUUID(self, project_name: str, iteration: str):
        """
        获取项目下具体迭代的uuid信息
        :param project_name: 项目名称
        :param iteration: 迭代版本
        :return:
        """
        try:
            userProject_iteration_list = json.loads(self.get_userProject_iteration_list(project_name))['sprints']
            for i in userProject_iteration_list:
                if i['title'] == iteration:
                    userProject_iterationUUID = i['uuid']
                    return userProject_iterationUUID
            return '没有找到相关项目或迭代信息！'
        except BaseException as e:
            self.logger.error('get_userProject_iterationUUID:' + str(e))

    def get_testcaseLibrary_list(self):
        """
        获取用例库列表信息，查询相关用例库信息包含uuid，返回json格式
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teams_uuid}/items/graphql'.format(
                teams_uuid=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            graphql = {
                "query": "query QUERY_LIBRARY_LIST{"
                         "testcaseLibraries(orderBy:{isPin:DESC\n namePinyin:ASC\n    }\n  ){\n    uuid,\n    name,\n    isPin,\n    isSample,\n    testcaseCaseCount,\n    testcaseFieldConfig{\n      key,\n      uuid,\n      name\n    }\n  }\n}",
                "variables": {}}
            ret = requests.post(url=request_URL, headers=headers, json=graphql)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            self.logger.error('get_case_library_list:' + str(e))

    def getCaseLibraryCaseList(self, testcaseLibrary_name: str):
        """
        获取用例库下的用例列表，testcaseLibrary_name：用例库名称 返回testcase_uuid列表信息
        :param testcaseLibrary_name:
        :return:
        """
        try:
            case_library_dist = json.loads(self.get_testcaseLibrary_list())['data']['testcaseLibraries']
            testcase_uuid = []  # 获取测试用例uuid
            for i in case_library_dist:
                if i['name'] == testcaseLibrary_name:
                    testcaseLibrary_uuid = i['uuid']  # 获取用例库的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/library/{libraryUUID}/cases'.format(
                        teamUUID=self.teams_uuid, libraryUUID=testcaseLibrary_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    for testcase in ret.json()["cases"]:  # 获取每条测试用例的uuid信息并存到列表中
                        testcase_uuid.append(testcase["uuid"])
                    return testcase_uuid
            return '没有找到用例库!'
        except BaseException as e:
            self.logger.error('getCaseLibraryCaseList:' + str(e))

    def getTestPlanList(self):
        """
        获取当前用户下测试计划列表相关信息,返回json格式
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plans'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            self.logger.error('getTestPlanList:' + str(e))

    def addCaseToCaseLibrary(self, testcase: dict, testcaseLibrary: str):
        """
        添加测试用例到用例库 ,testcase测试用例字典组；testcaseLibrary：用例库名称
        用例模板：
        testcase ={
            "item": {
            "name": "测试用例",              # 测试用例标题
            "assign": "VYNS7KSW",            # 负责人
            "priority": "CeF3DFD1",         # 优先级
            "type": "2XpDJNDU",             # 用例类型
            "module_uuid": "W42RK92P",      # 用例直属模块
            "condition": "11",              # 前置条件
            "library_uuid": "4y54Saz6",     # 用例库uuid
            "desc": "",                     # 用例描述
            "steps": [{                     # 执行步骤
                "id": 1,
                "desc": "11",               # 描述
                "result": ""                # 期望
            }, {
                "id": 2,
                "desc": "11",
                "result": ""
            }, {
                "id": 3,
                "desc": "11",
                "result": ""
            }],
            "related_wiki_page": [],       # 关联wiki界面
            "testcase_case_steps": [{      # 操作步骤
                "id": 1,
                "desc": "11",
                "result": ""
            }, {
                "id": 2,
                "desc": "11",
                "result": ""
            }, {
                "id": 3,
                "desc": "11",
                "result": ""
            }],
            "item_type": "testcase_case",   # 类型，不需要改
            "testcase_library": "4y54Saz6",  # 用例库uuid
            "testcase_module": "W42RK92P"   # 模块uuid
            }
        }
        :param testcase:
        :param testcaseLibrary:
        :return:
        """
        try:
            case_library_dist = json.loads(self.get_testcaseLibrary_list())['data']['testcaseLibraries']
            for i in case_library_dist:
                if i['name'] == testcaseLibrary:
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/items/add'.format(
                        teamUUID=self.teams_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers, json=testcase)
                    return ret.json()
        except BaseException as e:
            self.logger.error('addCaseToCaseLibrary:' + str(e))

    def getTestCaseList(self, testplan_name: str):
        """
        获取测试计划中的测试用例信息; testplan_name:测试计划
        :param testplan_name:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testplan_name:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{planUUID}/cases'.format(
                        teamUUID=self.teams_uuid, planUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    return ret.json()
            self.logger.error('getTestCaseList: 没有找到测试计划！')
            return '没有找到测试计划'
        except BaseException as e:
            self.logger.error('getTestCaseList: ' + str(e))

    def getTestCaseListName(self,testPlanName)->list:
        """
        获取测试计划中的测试用例，返回所有用例名称列表
        :param testPlanName:
        :return:
        """
        try:
            getList = self.getTestCaseList(testPlanName)['cases']
            TestCaseList = []
            for testcase in getList:
                TestCaseList.append({"uuid":testcase['uuid'],"number":testcase['number'],"name":testcase['name'],"executor":testcase['executor']})
            return TestCaseList
        except BaseException as e:
            self.logger.error('getTestCaseList:' + str(e))

    def getTestPlanTestCaseID(self, testPlan, testCase) -> str:
        """
        获取测试计划中的测试用例ID
        :param testPlan:
        :param testCase:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testPlan:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{planUUID}/cases'.format(
                        teamUUID=self.teams_uuid, planUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    cases_list = ret.json()['cases']
                    for case in cases_list:
                        if case['name'] == testCase:
                            testcaseID = case['number']
                            return testcaseID
            return '没有找到测试计划！'
        except BaseException as e:
            self.logger.error('getTestPlanTestCaseID: ' + str(e))

    def getTestCaseALLUUID(self, testPlanName, testCaseName):
        """
        获取测试计划中的测试用例所有的uuid,返回testcase_ALLUUID字典
        :param testPlanName: 测试计划名称
        :param testCaseName: 测试用例名称
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testPlanName:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{planUUID}/cases'.format(
                        teamUUID=self.teams_uuid, planUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    cases_list = ret.json()['cases']
                    testcase_stepsUUID = []  # 测试用例步骤的uuid
                    for case in cases_list:
                        if case['name'] == testCaseName:
                            testcaseID = case['number']
                            testcase = json.loads(self.getTestCaseInfo(testcaseID, testPlanName))['cases'][
                                0]  # 测试用例信息
                            testcaseUUID = testcase['uuid']
                            testcaseName = testcase['name']
                            testcaseNumber = testcase['number'] # case id
                            stepsUUID_list = testcase['steps']
                            for stepsUUID in stepsUUID_list:
                                testcase_stepsUUID.append(stepsUUID['uuid'])
                            testcase_ALLUUID = {
                                'testcaseUUID': testcaseUUID,  # 测试用例uuid
                                'testcaseName': testcaseName,  # 测试用例名称
                                'testcaseNumber': testcaseNumber, # 测试用例 id
                                'stepsUUID': testcase_stepsUUID  # 测试步骤的uuid
                            }
                            return testcase_ALLUUID
            return False # 没有找到测试计划或者测试用例！
        except BaseException as e:
            self.logger.error('ggetTestCaseALLUUID: ' + str(e))

    def validationTestCase(self, testPlanName, testCaseName)->bool:
        """
        校验测试用例,返回bool
        :param testPlanName: 测试计划名称
        :param testCaseName: 测试用例名称
        :return:
        """
        try:
            val_testcase = self.getTestCaseALLUUID(testPlanName, testCaseName)
            if val_testcase == False:
                return False
            elif val_testcase['testcaseName'] == testCaseName:
                return True
            else:
                return False
        except BaseException as e:
            self.logger.error('validationTestCase: ' + str(e))

    def greateTestPlan(self, testPlanTitle, relatedProject, relatedSprint):
        """
        创建测试计划
        :param testPlanTitle: 测试计划标题
        :param relatedProject: 关联项目
        :param relatedSprint: 关联迭代
        :return:
        """
        try:
            related_project_uuid = self.get_userProjectUUID(relatedProject)  # 获取关联项目uuid
            related_sprint_uuid = self.get_userProject_iterationUUID(relatedProject, relatedSprint)  # 获取迭代uuid
            testplan_content = {
                "plan": {
                    "name": testPlanTitle,  # 测试计划标题
                    "assigns": [self.user_uuid],  # 测试计划负责人，传self.user_uuid
                    "members": [{  # 参与测试人员
                        "user_domain_type": "testcase_plan_assign",  # 用户域（默认）
                        "user_domain_param": ""  # 用户域参数
                    }, {
                        "user_domain_type": "testcase_administrators",  # 管理员（默认）
                        "user_domain_param": ""
                    }],
                    "related_project_uuid": related_project_uuid,  # 关联项目uuid
                    "plan_stage": "BjAYD49R",  # 测试阶段:集成测试
                    "related_sprint_uuid": related_sprint_uuid,  # 关联迭代uuid
                    "related_issue_type_uuid": "8YtVcwaj",  # 缺陷对应工作项类型uuid
                    "check_points": [{  # 开始状态（默认）
                        "case_result": "passed",
                        "check_point": "note",
                        "is_must": False},
                        {
                            "case_result": "skipped",
                            "check_point": "file",
                            "is_must": False
                        }, {
                            "case_result": "passed",
                            "check_point": "note",
                            "is_must": False
                        }, {
                            "case_result": "passed",
                            "check_point": "file",
                            "is_must": False
                        }, {
                            "case_result": "failed",
                            "check_point": "note",
                            "is_must": False
                        }, {
                            "case_result": "failed",
                            "check_point": "file",
                            "is_must": False
                        }, {
                            "case_result": "blocked",
                            "check_point": "note",
                            "is_must": False
                        }, {
                            "case_result": "blocked",
                            "check_point": "file",
                            "is_must": False
                        }]
                },
                "is_update_default_config": True  # 是否更新关联项目默认配置
            }
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plans/add'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.post(url=request_URL, headers=headers, json=testplan_content)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            self.logger.error('greateTestPlan: ' + str(e))

    def deleteTestPlan(self, testPlanName: str):
        """
        删除测试计划，testPlanName：测试计划名称
        返回json格式
        {
          "code": 200,
          "errcode": "OK",
          "type": "OK"
        }
        :param testPlanName:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testPlanName:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com//project/api/project/team/{teamUUID}/testcase/plan/{testplanUUID}/delete'.format(
                        teamUUID=self.teams_uuid, testplanUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers)
                    return ret.text
            return '没有找到测试计划！'
        except BaseException as e:
            self.logger.error('deleteTestPlan: ' + str(e))

    def addCaseToTestPlan(self, testcase_group: dict, testPlan: str):
        """
        添加测试用例到测试计划中，testcase_group：测试用例组,testPlan：测试计划名称
        测试用例组：
        {
         "case_uuids": [
             "36B9ztJE",     # 测试⽤例UUID
             "XsxrqQJS"]
        }
        :param testcase_group:
        :param testPlan:
        :return:
        """
        try:
            testcase = {
                "case_uuids": testcase_group
            }
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testPlan:
                    plan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{testplanUUID}/cases/add'.format(
                        teamUUID=self.teams_uuid, testplanUUID=plan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers, json=testcase)
                    return ret.json()
        except BaseException as e:
            self.logger.error('addCaseToTestPlan: ' + str(e))

    def deleteTestPlanCase(self, testcase_group: dict, testPlan: str):
        """
        删除测试计划中的测试用例，testcase_group：要删除测试用例uuid组，testPlan：测试计划名称
        测试用例组：
        {
         "case_uuids": [
             "36B9ztJE",     # 测试⽤例UUID
             "XsxrqQJS"]
        }
        :param testcase_group:
        :param testPlan:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testPlan:
                    plan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{testplanUUID}/cases/delete'.format(
                        teamUUID=self.teams_uuid, testplanUUID=plan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers, json=testcase_group)
                    return ret.json()
        except BaseException as e:
            self.logger.error('deleteTestPlanCase: ' + str(e))

    def getTestCaseInfo(self, testcase_id: int, testplan: str):
        """
        获取测试计划中测试用例详细信息，testcase_id：测试用例ID，testplan：测试计划名称
        :param testcase_id:
        :param testplan:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testplan:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/search?key={key}&plan_uuid={plan_uuid}'.format(
                        teamUUID=self.teams_uuid, key=str(testcase_id), plan_uuid=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.get(url=request_URL, headers=headers)
                    # json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
                    return ret.json()
        except BaseException as e:
            self.logger.error('getTestCaseInfo: ' + str(e))

    def updateTestCaseStatus(self, testcase: dict, testplan: str):
        """
        更新测试计划中的测试用例，testcase:测试用例，testplan:测试计划名称
        测试用例模板
        {
            "cases": [{
                "uuid": "7QMWVLLi",               # 测试用例uuid
                "executor": "VYNS7KSW",           # 执行者 uuid
                "note": "测试",                   # 备注
                "result": "passed",               # 测试结果
                "steps": [{                       # 执行步骤
                    "uuid": "TM6UJ5CZ",           # 执行步骤uuid
                    "actual_result": "ces ",      # 执行步骤备注
                    "execute_result": "passed"    # 执行步骤结果
                }, {
                    "uuid": "MWcrefo8",
                    "actual_result": "ccc",
                    "execute_result": "passed"
                }, {
                    "uuid": "PHhRaY3E",
                    "actual_result": "cc",
                    "execute_result": "passed"
                }]
            }],
            "is_batch": false                   # 是否批量
        }
        :param testcase:
        :param testplan:
        :return:
        """
        try:
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testplan:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{testplanUUID}/cases/update'.format(
                        teamUUID=self.teams_uuid, testplanUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers, json=testcase)
                    return ret.json()
            return '没有找到相关测试用例！'
        except BaseException as e:
            self.logger.error('updateTestCaseStatus: ' + str(e))

    def update_testplan_status(self, status: str, testplan: str):
        """
        更新测试计划状态，testplan:测试计划名称
        进行中：{"status":"PGVpVbQK"}
        未开始：{"status":"WDQzS8M1"}
        已结束：{"status":"BCMGg76p"}
        :param status:
        :param testplan:
        :return:
        """
        try:
            status_info = {
                '未开始': 'WDQzS8M1',
                '进行中': 'PGVpVbQK',
                '已结束': 'BCMGg76p'
            }
            udate_status = {
                'status': status_info[status]
            }
            testplan_list = json.loads(self.getTestPlanList())['plans']
            for i in testplan_list:
                if i['name'] == testplan:
                    testplan_uuid = i['uuid']  # 获取测试计划的uuid
                    request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/testcase/plan/{testplanUUID}/update_status'.format(
                        teamUUID=self.teams_uuid, testplanUUID=testplan_uuid)
                    headers = {
                        'Ones-Auth-Token': self.user_token,
                        'Ones-User-Id': self.user_uuid,
                    }
                    ret = requests.post(url=request_URL, headers=headers, json=udate_status)
                    return ret.json()
            return '没有找到相关测试用例！'
        except BaseException as e:
            self.logger.error('update_testplan_status:' + str(e))

    def uploadAttachmentToCase(self, fileAddress: str, caseUuid: str, fileName: str, description: str,):
        """
        上传附件文件到测试用例中
        :param fileAddress:文件地址
        :param fileName:文件
        :param description:备注
        :param caseUuid:测试用例uuid
        :return:
        """
        try:
            # 上传资源
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/res/attachments/upload'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            request = {
                'description': description,
                'name': fileName,
                'ref_id': caseUuid,
                'ref_type': 'plan_case',
                'type': 'attachment'
            }
            ret = requests.post(url=request_URL, headers=headers, json=request)
            # 上传文件
            request_URL = 'https://ones.standard-robots.com/api/project/files/upload'
            data = {"token": ret.json()['token']} # 其他参数通过data传入即可
            files = {"file": open(fileAddress, 'rb')}
            time.sleep(1)
            ret = requests.post(url=request_URL, files=files,data=data)
            print(ret.text)
            return ret.json()
        except BaseException as e:
            self.logger.error('uploadAttachmentToTestcase:' + str(e))

    def get_testcase_resource(self, resource_uuid: str):
        """
        获取测试用例的附件
        :param resource_uuid: 附件uuid
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/plancase/case/{resource_uuid}/resource'.format(
                teamUUID=self.teams_uuid,resource_uuid=resource_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            self.logger.info('get_testcase_resource:'.format(ret))
        except BaseException as e:
            self.logger.error('get_testcase_resource: '+ str(e))

    def getTeamUserInfo(self, userUuid: str)->dict:
        """
        获取团队里的成员信息
        :return:
        """
        try:
            request_URL = f'https://ones.standard-robots.com/api/project/team/{self.teams_uuid}/member/{userUuid}'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            return ret.json() # 成员详细信息
        except BaseException as e:
            self.logger.error(f'getTeamUserInfo:{e}')


    #####################################################
    # Project API
    #####################################################
    def get_ProjectTask_items(self):
        """
        获取项目里所有工作项内容,返回task_Info_List信息（只获取进行中的任务状态）
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/items/graphql'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            graphql = {
                "query": "{\n  buckets(groupBy: {tasks: {}}, pagination: {limit: 50, after: \"\", preciseCount: true}) {\n    tasks(filterGroup: $filterGroup, orderBy: $orderBy, includeAncestors: {pathField: \"path\"}, orderByPath: \"path\", limit: 1000) {\n      key\n      name\n      uuid\n      serverUpdateStamp\n      path\n      subTaskCount\n      subTaskDoneCount\n      position\n      status {\n        uuid\n        name\n        category\n      }\n      deadline\n      subTasks {\n        uuid\n      }\n      issueType {\n        uuid\n      }\n      subIssueType {\n        uuid\n      }\n      project {\n        uuid\n      }\n      parent {\n        uuid\n      }\n      estimatedHours\n      remainingManhour\n      issueTypeScope {\n        uuid\n      }\n      _zTD1tRfa {\n        bgColor\n        color\n        uuid\n        value\n        position\n      }\n      name\n      status {\n        uuid\n        name\n      }\n      assign {\n        key\n        uuid\n        name\n        avatar\n      }\n      _Nj2xP8YJ\n      _N3jBnJs7\n      _89sptWCd\n      _EURcRZ3M\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n",
                "variables": {
                    "groupBy": 'null',
                    "orderBy": {
                        "position": "ASC",
                        "createTime": "DESC"
                    },
                    "filterGroup": [{
                        "project_in": ["VYNS7KSWFaUam5Ko"], # 项目UUID
                        "issueType_in": ["B7aTPV3N"]
                    }],
                    "bucketOrderBy": 'null',
                    "search": {
                        "keyword": "",
                        "aliases": []
                    }
                }
            }
            ret = requests.post(url=request_URL, headers=headers, json=graphql)
            json_ret = ret.json()['data']['buckets'][0]['tasks'] # 获取任务列表
            task_Info_List = []
            for task_info in json_ret: # 获取每个任务信息
                task_info_status = task_info['status']['category'] # 任务状态
                task_info_uuid = task_info['uuid'] # 任务uuid
                task_info_name = task_info['name'] # 任务名称
                if task_info_status == 'in_progress': # 任务处于进行中 to_do:未开始
                    task_Info = {
                        'task_name': task_info_name,
                        'task_uuid': task_info_uuid
                    }
                    task_Info_List.append(task_Info)
            return task_Info_List
        except BaseException as e:
            self.logger.error('get_ProjectTask_items: ' + str(e))

    def getProjectTaskTransitions(self, task_uuid) -> dict:
        """
        获取项目中的工作项具体信息,返回 task_Transitions_Info信息
        :param task_uuid: 任务uuid
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/task/{task_uuid}/info'.format(
                teamUUID=self.teams_uuid, task_uuid=task_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            task_Transitions_info = ret.json() # 获取任务下具体信息
            assignUuid = task_Transitions_info['assign'] # 获取负责人uuid
            for module in task_Transitions_info['field_values']: # 遍历所有模块的值
                if module['field_uuid'] == 'N3jBnJs7': # AGV IP
                    AGV_IP = module['value']
                if module['field_uuid'] == '89sptWCd': # 设备IP
                    Device_IP = module['value']
            try:
                related_testcase_plans = task_Transitions_info['related_testcase_plans'][0]['name']
            except BaseException :
                related_testcase_plans = ''
            task_Transitions_Info = {
                'uuid': task_Transitions_info['uuid'], # 工作项uuid
                'summary': task_Transitions_info['summary'], # 工作项标题
                "assign" : self.getTeamUserInfo(assignUuid)['name'], # 负责人名称
                'AGV_IP' : AGV_IP, # AGV IP
                'Device_IP': Device_IP, # 设备IP
                'related_testcase_plans': related_testcase_plans,# 关联到测试计划
            }
            return task_Transitions_Info
        except BaseException as e:
            self.logger.error('getProjectTaskTransitions:' + str(e))

    def update_ProjectTask_field_values(self, task_uuid: str, field_values: dict):
        """
        更新项目中的任务模块的状态值
        :param task_uuid: 任务uuid
        :param field_values: 需要更新的任务模块字段信息，dict格式:{"field_uuid": "Nj2xP8YJ", "type": 3, "value": 6000000} # 更新执行进度
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/tasks/update3'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            update_field_values = {
                "tasks": [
                        {"uuid": task_uuid,
                         "field_values": [field_values]}
                ]
            }
            ret = requests.post(url=request_URL, headers=headers, json=update_field_values)
            return ret.text
        except BaseException as e:
            print(e)

    def update_ProjectTask_Status(self, task_uuid: str, status: str):
        """
        更新项目任务状态
        :param task_uuid: 任务uuid
        :param status: 状态:未开始，进行中，已完成 注明：需要在进行中--》已完成
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/task/{task_uuid}/new_transit'.format(
                teamUUID=self.teams_uuid,task_uuid=task_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            if status == "已完成": status = '5QxSuRqK'
            if status == "未开始": status = '"SZkqEE7m'
            if status == '进行中': status = 'MYxkjZMG'
            update_status = {"transition_uuid":status}
            ret = requests.post(url=request_URL, headers=headers, json=update_status)
            return ret.text
        except BaseException as e:
            print(e)

    def uploadProjectTaskResource(self, fileAddress: str, task_uuid: str, fileName: str, description: str):
        """
        Project任务中上传文件;附件
        可参考：https://www.cnblogs.com/xiaocaicai-cc/p/14148640.html
        :param fileAddress:文件地址
        :param task_uuid:任务uuid
        :param fileName:文件名
        :param description:备注
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/res/attachments/upload'.format(
                teamUUID=self.teams_uuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            request = {
                'description': description,
                'name': fileName,
                'ref_id': task_uuid,
                'ref_type': 'task',
                'type': 'attachment'
            }
            ret = requests.post(url=request_URL, headers= headers,data = json.dumps(request))
            retToken = ret.json()['token']
            request_URL = 'https://ones.standard-robots.com/api/project/files/upload'
            data = {'token': retToken} # 其他参数使用data传递即可
            files = {'file':open(fileAddress, 'rb')}
            ret = requests.post(url=request_URL,data=data, files=files)
            return ret.json()
        except BaseException as e:
            self.logger.error('uploadProjectTaskResource: ' + str(e))

    def getProjectAttachments(self,ProjectUuid:str):
        """
        获取项目相关附件资源列表,车载系统自动化任务发布projectUuid:VYNS7KSWFaUam5Ko
        :param ProjectUuid:
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/project/{projectUUID}/attachments'.format(
                teamUUID=self.teams_uuid, projectUUID=ProjectUuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            return ret.json()
        except BaseException as e:
            self.logger.error('getProjectAttachments: ' +str(e))

    def getProjectTaskAttachments(self,taskUuid:str):
        """
        获取任务相关附件资源列表
        :param taskUuid:
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/task/{taskUUID}/attachments'.format(
                teamUUID=self.teams_uuid, taskUUID=taskUuid)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            return ret.json()
        except BaseException as e:
            self.logger.error('getProjectTaskAttachments: ' + str(e))

    def getTaskAttachmentsInfo(self,attachmentUUID:str):
        """
        获取任务/消息附件资源详情，包括下载资源所需要的临时 url
        :param attachmentUUID:
        :return:
        """
        try:
            request_URL = 'https://ones.standard-robots.com/project/api/project/team/{teamUUID}/res/attachment/{attachmentUUID}'.format(
                teamUUID=self.teams_uuid, attachmentUUID=attachmentUUID)
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_URL, headers=headers)
            return ret.json()
        except BaseException as e:
            self.logger.error('getProjectTaskAttachments: ' + str(e))

    def downloadTaskAttachments(self,taskUuid:str,fileName:str):
        """
        下载任务里中文件
        :param taskUuid:
        :param fileName:
        :return:
        """
        try:
            ret = self.getProjectTaskAttachments(taskUuid)
            for file in ret['attachments']:
                if file['name'] == fileName:
                    url = self.getTaskAttachmentsInfo(file['uuid'])['url']
                    ret = requests.get(url=url, stream=True)
                    with open('{0}{1}'.format(self.fileDownloadPath,fileName), 'wb') as code:
                        for chunk in ret.iter_content(chunk_size=512):
                            code.write(chunk)
                    self.logger.info('{} download completed!'.format(fileName) )
        except BaseException as e:
            self.logger.error('downloadTaskAttachments:' + str(e))

class Status_Analyze():
    """Testcase状态解析类"""

    def testResult(self, result: str):
        """
        测试执行结果
        :param result:
        :return:
        """
        status = {
            '通过': 'passed',
            '失败': 'failed',
            '阻塞': 'blocked',
            '跳过': 'skipped'
        }
        return status[str(result)]