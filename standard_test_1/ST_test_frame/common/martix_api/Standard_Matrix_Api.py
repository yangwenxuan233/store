# -*- coding:utf-8 -*-
# Standard Matrix HTTP API
# 新增Http v1.1接口
# Author: weisen
# time:20210915


import requests
import json
import prettytable as pt
import time
import os


class SR_Matrix_HTTP():

    def __init__(self, ip: str):
        """
        该类主要是使用HTTP接口去获取相关信息,例如地图导出，固件升级等等
        使用方式：
        agv_53 = SR_Matrix_HTTP('192.168.33.53')
        print(agv_53.get_mission_list()
        :param ip: AGV IP
        """
        self.ip = ip

    def login(self, account):
        """
        登录接口,不传密码
        :param account: 登录账号
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/account/{account}?type=username'.format(ip=self.ip, account=account)
            ret = requests.get(url=request_URL)
            return ret.json()
        except BaseException as e:
            print('login:' + str(e))

    def get_accounts(self):
        """
        获取所有用户信息,以列表形式返回
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/accounts'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            return ret.json()
        except BaseException as e:
            print('get_accounts: {}'.format(e))

    def get_mission_list(self):
        """
        获取mission列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/2/missions'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            dict_ret = ret.json()
            for x in dict_ret:
                del x['body']  # 去除body部分
            return json.dumps(dict_ret, ensure_ascii=False, indent=2, sort_keys=False)
        except BaseException as e:
            print('get_mission_list:' + str(e))

    def delete_mission_task(self, mission_id: int):
        """
        删除mission任务
        :param mission_id: 任务id
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission/{mission_id}'.format(ip=self.ip, mission_id=mission_id)
            ret = requests.delete(url=request_URL)
            ret = ret.text
            return ret
        except BaseException as e:
            print('delete_mission_task:' + str(e))

    def clear_mission_record(self):
        """
        清除mission记录
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission_record/clear'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            ret_test = ret.text
            return ret_test
        except BaseException as e:
            print('clear_mission_record: {}'.format(e))

    def get_map_list(self):
        """
        获取地图列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/map'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_map_list:' + str(e))

    def get_map_json(self, map_name: str):
        """
        获取地图json文件
        :param map_name:地图名称
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/map/{map_name}/data'.format(ip=self.ip, map_name=map_name)
            ret = requests.get(url=request_URL, stream=True)
            ret_json = json.dumps(ret.json(), ensure_ascii=False, indent=1, sort_keys=False)  # 格式转成json字符串
            with open('{}.json'.format(map_name), 'w') as code:
                code.write(ret_json)
        except BaseException as e:
            print('get_map_json:' + str(e))

    def get_map_image(self, map_name: str):
        """
        获取地图PNG图片
        :param map_name: 地图名称
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/map/{map_name}/image'.format(ip=self.ip, map_name=map_name)
            ret = requests.get(url=request_URL, stream=True)
            with open('{}.png'.format(map_name), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=512):
                    code.write(chunk)
        except BaseException as e:
            print('get_map_image:' + str(e))

    def get_task_template(self):
        """
        获取任务模板列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission_template?id=0'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            dict_ret = ret.json()
            for i in dict_ret:
                del i['body']  # 去除body部分
            return json.dumps(dict_ret, ensure_ascii=False, indent=2, sort_keys=False)
        except BaseException as e:
            print('get_task_template: ' + str(e))

    def get_mission_plan(self):
        """
        获取任务计划列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/schedule/get'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_mission_plan:' + str(e))

    def export_task(self, task_id: int):
        """
        导出任务脚本
        :param task_id: 任务id
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/mission/{task_id}/export'.format(ip=self.ip, task_id=task_id)
            ret = requests.get(url=request_URL, stream=True)
            with open('{}.task_export'.format(task_id), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=512):
                    code.write(chunk)
            self.logger.info('任务脚本下载完成')
        except BaseException as e:
            print('export_task: {}'.format(e))

    def get_account_management_list(self):
        """
        获取账号管理列表
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/accounts'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_account_management_list:' + str(e))

    def get_system_maintenance(self):
        """
        获取系统维护信息,返回最新的SROS、SRC升级记录
        :return:
        """
        try:
            SROS_request_URL = 'http://{ip}/api/v0/upgrade_record/system'.format(ip=self.ip)  # SROS升级记录
            SROS_ret = requests.get(url=SROS_request_URL)
            SRC_request_URL = 'http://{ip}/api/v0/upgrade_record/src'.format(ip=self.ip)  # SRC升级记录
            SRC_ret = requests.get(url=SRC_request_URL)
            SROS_upgrade_record = SROS_ret.json()  # SROS升级记录，最新记录是SROS_upgrade_record[0]
            SRC_upgrade_record = SRC_ret.json()  # SRC升级记录，最新记录是SRC_upgrade_record[0]
            return SROS_upgrade_record[0], SRC_upgrade_record[0]
        except BaseException as e:
            print('get_system_maintenance:' + str(e))

    def map_file_FMS_export(self, map_name: str):
        """
        地图文件导出-FMS格式,导出的地图会放在当前脚本目录下
        :param map_name: 地图文件名
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/map/{map_name}/export'.format(ip=self.ip, map_name=map_name)
            ret = requests.get(url=request_URL, stream=True)
            with open('{}_nav.map_export'.format(map_name), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=512):
                    code.write(chunk)
            print('下载完成')
        except BaseException as e:
            print('map_file_export:' + str(e))

    def map_file_FMS_import(self, map_address='') -> str:
        """
        地图导入，FMS方式导入，map_address:地图路径
        :param map_address: 地图路径
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/map/import'.format(ip=self.ip)
            files = {'file': open(map_address, 'rb')}  # 地图转成二进制读取
            print('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            return ret.text
        except BaseException as e:
            print('map_file_FMS_import:' + str(e))

    def get_config_parameter_list(self):
        """
        获取配置参数列表,返回json格式
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/setting'.format(ip=self.ip)  # SROS升级记录
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print(' get_config_parameter_list:' + str(e))

    def get_single_config_parameter(self, parameter_id: int):
        """
        获取单个配置参数详细信息
        :param parameter_id: 参数id,例如601
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/setting/{parameter_id}'.format(ip=self.ip, parameter_id=parameter_id)
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_single_config_parameter:' + str(e))

    def modify_single_parameter(self, parameter_id: int, modify_parameter: dict):
        """
        修改单个配置参数,修改的键值，例如：{'value':'1500'} 使用方式：self.modify_single_parameter(601,{'value': '1000'})
        :param parameter_id: 参数id
        :param modify_parameter: 修改的键值，例如：{'value':'1500'}
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/setting/{parameter_id}'.format(ip=self.ip, parameter_id=parameter_id)
            ret = requests.patch(url=request_URL, json=modify_parameter)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('modify_single_parameter:' + str(e))

    def SROS_firmware_upgrade(self, firmware_address='') -> str:
        """
        SROS固件升级，firmware_address 固件地址，返回<class 'web.webapi.OK'>
        :param firmware_address:固件地址
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/update/import'.format(ip=self.ip)
            files = {'file': open(firmware_address, 'rb')}  # 固件转成二进制读取
            self.logger.info('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            self.logger.info(ret.text)
            return ret.text
        except BaseException as e:
            print('SROS_firmware_upgrade:' + str(e))

    def SRC_firmware_upgrade(self, firmware_address='') -> str:
        """
        SRC(SRTOS)固件升级，firmware_address 固件地址，返回<class 'web.webapi.OK'>
        :param firmware_address:固件地址
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/src/import'.format(ip=self.ip)
            files = {'file': open(firmware_address, 'rb')}  # 固件转成二进制读取
            print('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            return ret.text
        except BaseException as e:
            print('SRC_firmware_upgrade:' + str(e))

    def SROS_firmware_rollback(self):
        """
        SROS固件回退，仅适用于SROS自身启动失败的情景，仅在dev权限使用，严禁向低权限的用户使用，返回'state':true表示回退成功
        {
          "state": true,
          "code": 9999,
          "data": {},
          "message": ""
        }
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/rollback/system'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('SROS_firmware_rollback:' + str(e))

    def get_system_startup_log(self, limit: int, offset=0):
        """
        获取系统启动日志
        :param offset: 开始位置，默认为0
        :param limit: 获取多少条数据，最大不能超出100条数据
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/log/startup'.format(ip=self.ip)
            parameter = {
                'offset': offset,
                'limit': limit
            }
            ret = requests.get(url=request_URL, params=parameter)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_system_startup_log:' + str(e))

    def get_system_log(self, lines: int):
        """
        获取系统日志信息
        +------------+---------------------------+---------------+------+-------------------------------+
        |  日志ID    |            时间           |      模块     | 等级 |              日志             |
        +------------+---------------------------+---------------+------+-------------------------------+
        | id:1168929 | 2021-09-18T17:57:48+08:00 | movement-task | info | Movement task 701 in running! |
        | id:1168930 | 2021-09-18T17:57:48+08:00 | movement-task | info | Movement task 701 in running! |
        +------------+---------------------------+---------------+------+-------------------------------+
        :param lines: 获取日志行数
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/userlog/follow?lines={lines}&level=info'.format(ip=self.ip, lines=lines)
            ret = requests.get(url=request_URL)
            tb = pt.PrettyTable()  # 输出表格格式化
            tb.field_names = ['日志ID  ', '时间', '模块', '等级', '日志']
            for i in ret.json()['logs']:
                tb.add_row(['id:{}'.format(i['id']), i['time'], i['key'], i['severity'], i['msg']])
            print(tb)
            json_ret = json.dumps(ret.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_ret
        except BaseException as e:
            print('get_system_log:' + str(e))

    def export_log(self):
        """
        导出部分调试日志
        :return:
        """
        try:
            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            request_URL = 'http://{ip}/api/v0/log/export'.format(ip=self.ip)
            print('日志正在下载...')
            ret = requests.get(url=request_URL, stream=True)
            flag = True
            if flag:
                path = r"./Dowmload/log/"
                if not os.path.exists(path):
                    os.makedirs(path)
            with open('./Dowmload/log/{ip}_SROS_{time}.log_export'.format(ip=self.ip, time=current_time), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=65535):
                    code.write(chunk)
            print('下载完成')
        except BaseException as e:
            print('export_log:' + str(e))

    def export_debug_log(self):
        """
        导出全部debug日志
        :return:
        """
        try:
            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            request_URL = 'http://{ip}/api/v0/log/export?debug=true'.format(ip=self.ip)
            print('日志正在下载...')
            ret = requests.get(url=request_URL, stream=True)
            with open('{ip}_SROS_{time}_debug.log_export'.format(ip=self.ip, time=current_time), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=512):
                    code.write(chunk)
            print('下载完成')
        except BaseException as e:
            print('export_debug_log:' + str(e))

    def export_config_db(self):
        """
        导出db数据库
        :return:
        """
        try:
            current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            request_URL = 'http://{ip}/api/v0/db'.format(ip=self.ip)
            print('数据库正在下载...')
            ret = requests.get(url=request_URL, stream=True)
            flag = True
            if flag:
                path = r"./Dowmload/db/"
                if not os.path.exists(path):
                    os.makedirs(path)
            with open('./Dowmload/db/{ip}_SROS_{time}.db_export'.format(ip=self.ip, time=current_time), 'wb') as code:
                for chunk in ret.iter_content(chunk_size=512):
                    code.write(chunk)
            print('下载完成')
        except BaseException as e:
            print('export_config_db:' + str(e))

    def import_config_db(self, db_address='') -> str:
        """
        导入config_db数据库，db_address=数据库地址
        :param db_address: 数据库地址
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/db'.format(ip=self.ip)
            files = {'file': open(db_address, 'rb')}  # 数据文件转成二进制读取
            print('正在上传文件...')
            ret = requests.post(request_URL, files=files)
            print(ret.text)
            return ret.text
        except BaseException as e:
            print('import_config_db:' + str(e))

    def roll_back_configuration(self):
        """
        回归配置参数,返回：state: true表示回滚成功；例如：{'state': True, 'code': 9999, 'data': {'is_exist_new_config_info': False}, 'message': ''}
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/config_info/rollback'.format(ip=self.ip)
            ret = requests.get(url=request_URL)
            return ret.json()
        except BaseException as e:
            print('export_debug_log:' + str(e))

    def import_logo(self, logo_address=''):
        """
        导入自定义logo文件
        :param logo_address: logo文件地址
        :return:
        """
        try:
            request_URL = 'http://{ip}/api/v0/logo_customize'.format(ip=self.ip)
            file = {'file': open(logo_address, 'rb')}
            ret = requests.post(request_URL, files=file)
            self.logger.info('正在上传文件...')
            return ret.text
        except BaseException as e:
            print('map_logo:' + str(e))
