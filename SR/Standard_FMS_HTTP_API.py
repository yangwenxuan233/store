import requests
import json


class FMSApi(object):
    """The built-in FMS API.
    """

    def __init__(self) -> None:
        self.base_url = 'http://172.28.1.68:8088/api/v2/'

    def set_token(self, token: str) -> None:
        self.token = token

    def get_token(self) -> str:
        return self.token

    def set_base_url(self, base_url) -> None:
        self.base_url = base_url

    def get_base_url(self) -> str:
        return self.base_url

    def login(self, username: str, password: str) -> str:
        '''FMS账号登录接口。(post)
        :param: username: 用户名, password: 密码
        :return: str
        '''
        try:
            request_url = self.base_url + 'session'
            json_request = {
                'username': username,
                'password': password
            }
            re = requests.post(url=request_url, json=json_request)  # response
            self.token = re.json()['token']
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('login: ' + str(e))

    def create_new_order(self, mission, appoint_vehile_id='', appoint_vehile_group='', priority=''):
        '''创建新订单接口。(post)
        :param:
            mission: 任务列表,
            appoint_vehile_id: 订单预约的车辆id,
            appoint_vehile_group: 指定的车型组id,
            priority: 任务优先级
        :type:
            dict{ move: [ [destination, map_id], ...],
                  action: [ [action_id, action_param1, action_param2], ...] }, int, int, int
        :return: str
        '''
        try:
            request_url = self.base_url + 'orders'
            json_request = {
                'appoint_vehicle_group': appoint_vehile_group,
                'appoint_vehicle_id': appoint_vehile_id,
                'mission': [],
                'priority': priority
            }
            # 解析并插入mission数据
            move_list = [mission['move']][0]
            print(move_list)
            action_list = [mission['action']][0]
            for i in move_list:
                json_request['mission'].append({
                    'destination': i[0],
                    'is_need_fail_strategy': False,
                    'map_id': i[1],
                    'type': 'move'
                })
            for j in action_list:
                json_request['mission'].append({
                    'action_id': j[0],
                    'action_name': '',
                    'action_param1': j[1],
                    'action_param2': j[2],
                    'action_template_id': 0,
                    'dst': "0",
                    'is_need_fail_strategy': False,
                    'is_pr:einstall': 0,
                    'type': 'act'
                })
            headers = {
                'token': self.token
            }
            print(json_request)
            re = requests.post(url=request_url, headers=headers, json=json_request)  # response
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('create_new_order: ' + str(e))

    def get_order_list(self, appoint_vehicle_id='', execute_vehicle_id=0, filter_by_source='',
                       filter_by_state=0, order='', order_by='', page=1, perpage=10, user_id='') -> str:
        '''获取订单列表。(get)
        :param:
            appoint_vehicle_id: 预约车辆id,
            execute_vehicle_id: 执行车辆id,
            filter_by_source: 订单来源过滤器* 1.WMS, 2.FMS,
            filter_by_state: 订单状态过滤器* 1.队列中, 2.已取消, 3.执行中, 4.已失败, 5.已成功, 6.已删除,
                                            7.手动暂停, 8.暂停执行(移除订单池), 9.已挂起, 10.队列外,
            order: 正序倒序(DESC为降序,ASC为正序),
            order_by: 排列的列名,
            page: 当前页数(默认为1),
            perpage: 每页数据个数(默认为10),
            user_id: 下发订单用户id
        :type: int, int, int, int, str, str, int, int, int
        :return: str
        '''
        try:
            request_url = self.base_url + 'orders?appoint_vehicle_id={appoint_vehicle_id}&execute_vehicle_id={execute_vehicle_id}&filter_by_source={filter_by_source}&filter_by_state={filter_by_state}&order={order}&order_by={order_by}&page={page}&perpage={perpage}&user_id={user_id}'.format(appoint_vehicle_id=appoint_vehicle_id, execute_vehicle_id=execute_vehicle_id, filter_by_source=filter_by_source, filter_by_state=filter_by_state, order=order, order_by=order_by, page=page, perpage=perpage, user_id=user_id)
            headers = {
                'token': self.token
            }
            re = requests.get(url=request_url, headers=headers)  # response
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('get_order_list: ' + str(e))

    def create_order_by_mould(self, order_template_id: int) -> str:
        '''通过订单模板创建订单接口。(post)
        :param: order_template_id: 订单模板id
        :return: str
        '''
        try:
            request_url = self.base_url + '/orders/template/{order_template_id}'.format(order_template_id=order_template_id)
            headers = {
                'token': self.token
            }
            json_request = {}
            re = requests.post(url=request_url, headers=headers, json=json_request)
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('create_order_by_mould: ' + str(e))

    def get_specific_order(self, order_id: int) -> str:
        '''获取指定订单信息接口。(get)
        命令执行成功时无响应返回。
        :param: order_id: 订单id
        :retrun: str
        '''
        try:
            request_url = self.base_url + 'orders/{order_id}'.format(order_id=order_id)
            headers = {
                'token': self.token
            }
            re = requests.get(url=request_url, headers=headers)  # response
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('get_specific_list: ' + str(e))

    def command_to_order(self, order_id: int, command_type: str) -> str:
        '''命令控制指定订单接口。(post)
        :param:
            order_id: 订单id
            command_type: 命令类型:
                CMD_ORDER_CANCEL: 订单取消,
                CMD_ORDER_REJECTED: 暂停执行(移除订单池),
                CMD_ORDER_CONTINUE_FROM_REJECTED: 从REJECTED状态恢复为队列中状态,
                CMD_ORDER_HELD: 在执行中手动暂停任务(人主动暂停),
                CMD_ORDER_CONTINUE_FROM_HELD: 从HELD状态恢复为队列中状态,
                CMD_ORDER_JUMP_FROM_HANG: 跳过当前子任务继续执行,
                CMD_ORDER_CONTINUE_FROM_HANG: 从当前子任务继续执行,
                CMD_ORDER_SORT_UP: 订单池排序提升,
                CMD_ORDER_SORT_DOWN: 订单池排序下降,
                CMD_ORDER_RECOVERY_FROM_QUEUED: 从QUEUED状态恢复为队列中状态
        :return: str
        '''
        try:
            request_url = self.base_url + '/orders/{order_id}/command'.format(order_id=order_id)
            headers = {
                'token': self.token
            }
            json_request = {
                'command_type': command_type
            }
            re = requests.post(url=request_url, headers=headers, json=json_request)
            print(re.status_code)
            # json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return re.text
        except Exception as e:
            print('command_to_order ' + str(e))

    def get_statistics(self, type, begin, end, filter='', group='VEHICLE', metrics='DAY',
                       metrics_start_time='08:00:00', metrics_interval_time='24') -> str:
        '''获取统计信息接口。(get)
        :param:
            type: 统计维度(可选择订单: order, 车辆: vehicle)
            begin: 统计开始时间(yyyy-MM-dd+HH:mm:ss)
            end: 统计结束时间(yyyy-MM-dd+HH:mm:ss)
            filter: 筛选编号。数组格式,英文逗号分割,如示例filter=12,13,14
            group: 统计的维度。根据统计类型可以分为两种:(默认值为VEHICLE)
                :订单存在: VEHICLE:车辆, SOURCE:用户(来源), TEMPLATE:模板, VEHICLE_GROUP:车型组, ALL 不分组,不传默认为全部
                :车辆存在: VEHICLE: 车辆
            metrics: 统计的时间粒度。(WEEK:周, MONTH:月, YEAR:年, DAY:日, HOUR:小时, MULTI_HOUR:多时间段。默认值为DAY)
            metrics_start_time: 统计开始时间。如设置08:00:00,统计会在08:00:00开始统计, 加上metrics_interval_time就是统计的前后时间。
                                (metrics为DAY和MULTI_HOUR时,这是必选项。默认值为08:00:00)
            metrics_interval_time: 统计时间范围。统计开始时间加上该时间范围,即可获得统计的前后时间,一般设置0~24小时。
                                (metrics为DAY和MULTI_HOUR时,这是必选项。默认值为24)
        :type: str, str, str, str, str, str, str, int
        :return: str
        '''
        try:
            request_url = self.base_url + 'statistics/{type}?begin={begin}&end={end}&filter={filter}&group={group}&metrics={metrics}&metrics_start_time={metrics_start_time}&metrics_interval_time={metrics_interval_time}'.format(type=type, begin=begin, end=end, filter=filter, group=group, metrics=metrics, metrics_start_time=metrics_start_time, metrics_interval_time=metrics_interval_time)
            headers = {
                'token': self.token
            }
            re = requests.get(url=request_url, headers=headers)
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('get_statistics: ' + str(e))

    def add_vehicle_to_system(self, nickname, ip_addr, mac_addr='') -> str:
        '''添加车辆到系统接口。(post)
        :param:
            nickname: 车辆识别名,需要保证在系统内唯一,
            ip_addr: 车辆ip地址,
            mac_addr: 车辆mac地址
        :type: str, str, str
        :return: str
        '''
        try:
            request_url = self.base_url + 'vehicles'
            headers = {
                'token': self.token
            }
            json_request = {
                'ip_addr': ip_addr,
                'mac_addr': mac_addr,
                'nickname': nickname
            }
            re = requests.post(url=request_url, headers=headers, json=json_request)
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('add_vehicle_to_system: ' + str(e))

    def get_vehicle_list(self, page=1, perpage=10, is_alive='all', is_online='all', is_working='all') -> str:
        '''获取车辆列表。(get)
        :param:
            is_alive: all(默认): 全部车辆, alive: 在线车辆, dead: 离线车辆,
            is_online: all(默认): 全部车辆, online: 可被调度车辆, offline: 不可被调度车辆,
            is_woking: all(默认): 全部车辆, woking: 正在执行任务车辆, free: 空闲车辆,
            page: 当前页数,
            perpage: 每页个数
        :type: str, str, str, int, int
        :return: str
        '''
        try:
            request_url = self.base_url + 'vehicles?page={page}&perpage={perpage}&is_alive={is_alive}&is_online={is_online}&is_working={is_working}'.format(page=page, perpage=perpage, is_alive=is_alive, is_online=is_online, is_working=is_working)
            headers = {
                'token': self.token
            }
            re = requests.get(url=request_url, headers=headers)
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('get_vehicle_list: ' + str(e))

    def command_to_vehicle(self, command_type, vehicle_id, param1='', param2='') -> str:
        '''向指定车发送命令接口。(post)
        命令执行成功时无响应返回。
        :param:
            command_type: 命令类型:
                CMD_VEHICLE_PAUSE_ALL: 所有车辆暂停,
                CMD_VEHICLE_CONTINUE_ALL: 所有车辆继续任务,
                CMD_VEHICLE_ONLINE_ALL: 所有车辆上线,
                CMD_VEHICLE_OFFLINE_ALL: 所有车辆下线,
                CMD_VEHICLE_CANCEL_EMERGENCY_ALL: 所有车辆取消急停,
                CMD_VEHICLE_TRIGGER_EMERGENCY_ALL: 所有车辆触发急停,
                CMD_VEHICLE_CANCEL_TASK_ALL: 所有车辆取消任务,
                CMD_VEHICLE_DISABLED_LOCATE: 停止定位,
                CMD_VEHICLE_UPDATE_ONLINE: 车辆上下线 (参数1:1为上线, 0为下线),
                CMD_VEHICLE_CHANGE_MAP: 切换地图 (参数1:地图名),
                CMD_VEHICLE_PAUSE: 暂停车辆正在执行的任务,
                CMD_VEHICLE_CONTINUE: 继续车辆正在执行的任务,
                CMD_VEHICLE_CANCEL_EMERGENCY: 取消车辆急停状态,
                CMD_VEHICLE_TRIGGER_EMERGENCY: 触发急停,
                CMD_VEHICLE_STATION_LOCATE: 根据站点定位 (参数1:站点id),
                CMD_VEHICLE_MANUAL_CONTROL: 设置车辆为手动控制状态,
                CMD_VEHICLE_CANCEL_MANUAL_CONTROL: 取消车辆为手动控制状态,
                CMD_VEHICLE_CANCEL_TASK: 取消车辆正在执行的任务,
                CMD_VEHICLE_SET_AUTOCROSS: 避障状态设置 (参数1:"true"为开启,"false"为关闭),
                CMD_VEHICLE_PASS: 结束车辆等待动作 (动作为131 0 0),
                CMD_VEHICLE_CHARGE: 一键充电
            vehicle_id: 目标车辆id,
            param1: 命令参数1,
            param2: 命令参数2
        :type: str, int, int, int
        :return: str
        '''
        try:
            request_url = self.base_url + 'vehicles/command'
            headers = {
                'token': self.token
            }
            json_request = {
                'command_type': command_type,
                'param1': param1,
                'param2': param2,
                'vehicle_id': vehicle_id
            }
            re = requests.post(url=request_url, headers=headers, json=json_request)
            print(re.status_code)
            return re.text
        except Exception as e:
            print('command_to_vehicle: ' + str(e))

    def get_specific_vehicle(self, vehicle_id: int) -> str:
        '''获取指定车辆信息。(get)
        :param: vehicle_id: 目标车辆id
        :return: str
        '''
        try:
            request_url = self.base_url + 'vehicles/{vehicle_id}'.format(vehicle_id=vehicle_id)
            headers = {
                'token': self.token
            }
            re = requests.get(url=request_url, headers=headers)
            json_re = json.dumps(re.json(), ensure_ascii=False, indent=2, sort_keys=False)
            return json_re
        except Exception as e:
            print('get_specific_vehicle: ' + str(e))

    def delete_vehicle_from_system(self, vehicle_id: int) -> str:
        '''从系统删除指定车辆接口。(delete)
        :param: vehicle_id: 目标车辆id
        :return: str
        '''
        try:
            request_url = self.base_url + 'vehicles/{vehicle_id}'.format(vehicle_id=vehicle_id)
            headers = {
                'token': self.token
            }
            re = requests.delete(url=request_url, headers=headers)
            return re.text
        except Exception as e:
            print('delete_vehicle_from_system: ' + str(e))


if __name__ == '__main__':
    FMS = FMSApi()
    FMS.login('dev', 'developer')
    # mission = {
    #     'move': [
    #         [3, 4],
    #     ],
    #     'action': [
    #         [4, 11, 50]
    #     ]
    # }
    # data = FMS.create_new_order(mission)
    data = FMS.get_vehicle_list()
    # data = FMS.add_vehicle_to_system('demo20220303', '192.168.33.222', 'aa:bb:cc:dd:ee:ff')
    # data = FMS.command_to_vehicle('CMD_VEHICLE_TRIGGER_EMERGENCY', 47, -1, -1)
    # data = FMS.get_specific_vehicle(47)
    # data = FMS.delete_vehicle_from_system(53)
    print(data)
    print(type(data))
