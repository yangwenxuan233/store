import requests
import json


class OnesApi(object):
    """The built-in ONES API
    # """

    def __init__(self):
        self.user_token = None
        self.user_uuid = None
        self.teams_uuid = None

    def login(self, email: str, password: str):
        """
        ONES账号登录接口
        :param email: 邮箱账号
        :param password: 密码
        :return:
        """
        try:
            request_url = 'https://ones.standard-robots.com/project/api/project/auth/login'
            json_request = {
                'email': email,
                'password': password
            }
            ret = requests.post(url=request_url, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            self.user_token = ret.json()['user']['token']  # 获取token
            self.user_uuid = ret.json()['user']['uuid']  # 获取用户id
            self.teams_uuid = ret.json()['teams'][0]['uuid']  # 获取用户在团队id
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def sign_out(self):
        """
        退出ONES登录,返回http_status_code=200或者null
        :return:
        """
        try:
            request_url = 'https://ones.standard-robots.com/project/api/project/auth/logout'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    # -----------department-------------------
    def department_inquire_list(self, team_uuid: str):
        """
        部门查询接口
        :param team_uuid: 团队uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/departments'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    def department_add(self, team_uuid: str, name: str, parent_uuid: str, next_uuid: str):
        """
        部门增加接口
        :param team_uuid: 团队uuid
        :param name: 部⻔名称  不为空
        :param parent_uuid: ⽗部⻔的UUID(⼦部⻔需要填写) 可以为空
        :param next_uuid: 下⼀个同级节点的UUID(不填默认为最后节点) 可以为空
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/departments/add'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                'name': name,
                'parent_uuid': parent_uuid,
                'next_uuid': next_uuid
            }
            ret = requests.post(url=request_url, json=json_request, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def department_update(self, team_uuid: str, depart_uuid: str, name: str, next_uuid: str, parent_uuid: str,
                          member_count: int):
        """
        部门更新接口
        :param team_uuid: 团队uuid
        :param depart_uuid: 部门uuid
        :param name: 部⻔名称  不为空
        :param parent_uuid: ⽗部⻔的UUID(⼦部⻔需要填写) 可以为空
        :param next_uuid: 下⼀个同级节点的UUID(不填默认为最后节点) 可以为空
        :param member_count: 当前部⻔成员数 不为为空
        :return: json update stamp
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/department/update/{depart_uuid}'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                'member_count': member_count,
                'name': name,
                'next_uuid': next_uuid,
                'parent_uuid': parent_uuid,
                'uuid': depart_uuid
            }
            ret = requests.post(url=request_url, json=json_request, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def department_delete(self, team_uuid: str, depart_uuid: str):
        """
        部门删除接口
        :param team_uuid: 团队uuid
        :param depart_uuid: 部门uuid
        :return: json update stamp
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/department/delete/{depart_uuid}'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.post(url=request_url, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    # -----------product-------------------
    def product_inquire(self, team_uuid: str):
        """
        产品查询接口
        :param team_uuid: 团队uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/items/graphql'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.post(url=request_url, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def product_add(self, team_uuid: str, assign: str, name: str, item_type: str):
        """
        产品增加接口
        :param team_uuid: 团队uuid
        :param assign: 负责人UUID
        :param name: 产品名称
        :param item_type: item类型
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/items/add'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                'item': {
                    "assign": assign,
                    "name": name,
                    "item_type": item_type
                }
            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def product_update(self, team_uuid: str, product_uuid: str, assign: str):
        """
        产品更新接口
        :param team_uuid: 团队uuid
        :param product_uuid: 产品uuid
        :param assign: 负责人UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/item/product-{product_uuid}/update'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                'item': {
                    "assign": assign,
                }
            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def product_delete(self, team_uuid: str, product_uuid: str):
        """
        产品更新接口
        :param team_uuid: 团队uuid
        :param product_uuid: 产品uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/item/product-{product_uuid}/delete'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.post(url=request_url, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def product_inquire_model_list(self, team_uuid: str):
        """
        产品模块下列表查询接口
        :param team_uuid: 团队uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/items/graphql'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.post(url=request_url, headers=headers)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    # -----------team-------------------
    def team_inquire(self, team_uuid: str):
        """
        团队信息查询接口
        :param team_uuid: 团队uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/info'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    def members_inquire(self, team_uuid: str):
        """
        成员信息查询接口
        :param team_uuid: 团队uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/members'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    def members_single_inquire(self, team_uuid: str, user_uuid: str):
        """
        单个成员信息查询接口
        :param team_uuid: 团队uuid
        :param user_uuid: 用户uuid
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/member/{user_uuid}'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    def members_join(self, team_uuid: str, depart_uuid: str, user_uuid: str):
        """
        成员加入接口
        :param team_uuid: 团队uuid
        :param depart_uuid: 部门UUID
        :param user_uuid: 成员UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/users/update/department'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "all": True,
                "departments_to_join": [depart_uuid],
                "query": "{ \n users(\n orderBy: {\n tag: DESC\n"
                         "namePinyin: ASC\n }\n \n filterGroup: [{\n \n \n"
                         "uuid_in: $selectedUserUUIDs\n status_in: $memberStatus\n }]\n"
                         "\n ){\n \n uuid\n name\n email\n \n }\n }",
                "variables": {
                    "selectedUserUUIDs": [user_uuid],
                    "memberStatus": [
                        "pending",
                        "disable",
                        "normal"]
                }
            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def members_leave(self, team_uuid: str, depart_uuid: str, user_uuid: str):
        """
        成员移除接口
        :param team_uuid: 团队uuid
        :param depart_uuid: 部门UUID
        :param user_uuid: 成员UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/users/update/department'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "all": True,
                "departments_to_leave": [depart_uuid],
                "query": "{ \n users(\n orderBy: {\n tag: DESC\n"
                         "namePinyin: ASC\n }\n \n filterGroup: [{\n \n \n"
                         "uuid_in: $selectedUserUUIDs\n status_in: $memberStatus\n }]\n"
                         "\n ){\n \n uuid\n name\n email\n \n }\n }",
                "variables": {
                    "selectedUserUUIDs": [user_uuid],
                    "memberStatus": ["pending", "disable", "normal"]
                }
            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def members_restore(self, organization_uuid: str, user_uuid: str):
        """
        成员启动接口
        :param organization_uuid: 组织UUID
        :param user_uuid: 成员UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/organization/{organization_uuid}/restore_members'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "all": True,
                "variables": {
                    "selectedUserUUIDs": [user_uuid],
                    "memberStatus": ["disable"]
                },
                "query": "{ \n users(\n orderBy: {\n tag: DESC\n"
                         "namePinyin: ASC\n }\n \n filterGroup: [{\n \n \n"
                         "uuid_in: $selectedUserUUIDs\n status_in: $memberStatus\n }]\n"
                         "\n ){\n \n uuid\n name\n email\n \n }\n }",

            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def members_disable(self, organization_uuid: str, user_uuid: str):
        """
        成员禁用接口
        :param organization_uuid: 组织UUID
        :param user_uuid: 成员UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/organization/{organization_uuid}/disable_members'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "all": True,
                "variables": {
                    "selectedUserUUIDs": [user_uuid],
                    "memberStatus": ["normal"]
                },
                "query": "{ \n users(\n orderBy: {\n tag: DESC\n"
                         "namePinyin: ASC\n }\n \n filterGroup: [{\n \n \n"
                         "uuid_in: $selectedUserUUIDs\n status_in: $memberStatus\n }]\n"
                         "\n ){\n \n uuid\n name\n email\n \n }\n }",

            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    def members_delete(self, organization_uuid: str, user_uuid: str):
        """
        成员删除接口
        :param organization_uuid: 组织UUID
        :param user_uuid: 成员UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{organization_uuid}/delete_members'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "all": True,
                "variables": {
                    "selectedUserUUIDs": [user_uuid],
                    "memberStatus": ["pending", "disable", "normal"]
                },
                "query": "{ \n users(\n orderBy: {\n tag: DESC\n"
                         "namePinyin: ASC\n }\n \n filterGroup: [{\n \n \n"
                         "uuid_in: $selectedUserUUIDs\n status_in: $memberStatus\n }]\n"
                         "\n ){\n \n uuid\n name\n email\n \n }\n }",

            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    # -----------user-------------------
    def user_inquire(self):
        """
        用户信息查询接口
        :return: json
        """
        try:
            request_url = 'https://ones.standard-robots.com/project/api/project/users/me'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            ret = requests.get(url=request_url, headers=headers)
            return ret.text
        except BaseException as e:
            print('sign_out:' + str(e))
            # self.logger.error('sign_out:' + str(e))

    def user_update(self, team_uuid: str, user_uuid: str, title: str, company: str, name: str, *department_uuids):
        """
        用户更新接口
        :param team_uuid: 团队uuid
        :param user_uuid: 用户uuid
        :param title: 职位
        :param company: 公司
        :param name: 用户名
        :param department_uuids: 所在部⻔的UUID
        :return: json
        """
        try:
            request_url = f'https://ones.standard-robots.com/project/api/project/team/{team_uuid}/users/update'
            headers = {
                'Ones-Auth-Token': self.user_token,
                'Ones-User-Id': self.user_uuid,
            }
            json_request = {
                "department_uuids": [str(i) for i in department_uuids],
                "name": name,
                "company": company,
                "title": title,
                "user_uuid": user_uuid,
                "license_types": [1, 2, 3, 4, 5]
            }
            ret = requests.post(url=request_url, headers=headers, json=json_request)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('login:' + str(e))
            # self.logger.error('login:' + str(e))

    # ------testapi----------------
    def greate_testplan(self, testplan_title, related_project, related_sprint) -> str:
        """
        创建测试计划，testplan_title：测试计划标题，related_project：关联项目，related_sprint：关联迭代
        :param testplan_title:
        :param related_project:
        :param related_sprint:
        :return:
        """
        try:
            related_project_uuid = self.get_userProjectUUID(related_project)  # 获取关联项目uuid
            related_sprint_uuid = self.get_userProject_iterationUUID(related_project, related_sprint)  # 获取迭代uuid
            testplan_content = {
                "plan": {
                    "name": testplan_title,  # 测试计划标题
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
            return ret.json()
        except BaseException as e:
            # self.logger.error('greate_testplan: ' + str(e))
            print('greate_testplan: ' + str(e))


if __name__ == "__main__":
    ones = OnesApi()
    str_res = ones.login('renxing@standard-robots.com', 'renxing@123')
    dic_res = json.loads(str_res)
    uuid = dic_res['teams'][0]['uuid']
    # print(ones.department_get_list('HUBTGFvi'))
