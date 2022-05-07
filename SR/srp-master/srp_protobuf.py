#!/usr/bin/env python
# -*- coding:utf-8 -*-



import hashlib
import main_pb2
import math
import frame as srp_frame
from log import Logging


class SrpProtobuf:
    '''本类处理protobuf协议的解析'''

    def __init__(self, write_callback, response_callback):
        self.systemfunctions = SystemFunctions()  # 系统功能组初始化
        self.logging = Logging
        self._session_id = 0
        self._frame = srp_frame.Frame(self._onNewMessageCallback)
        self._write = write_callback
        self._response_callback = response_callback
        self._system_state_callback = None
        self._hardware_state_callback = None
        self._laser_point_callback = None
        self._notify_move_task_finished_callback = None
        self._notify_action_task_finished_callback = None
        self._notify_mission_list_change_callback = None
        self._last_action_state = main_pb2.ActionTask.TaskState.AT_ZERO

    def set_system_state_callback(self, fun):
        self._system_state_callback = fun

    def set_hardware_state_callback(self, fun):
        self._hardware_state_callback = fun

    def set_laser_point_callback(self, fun):
        self._laser_point_callback = fun

    def set_notify_move_task_finished_callback(self, fun):
        self._notify_move_task_finished_callback = fun

    def set_notify_action_task_finished_callback(self, fun):
        self._notify_action_task_finished_callback = fun

    def set_notify_mission_list_change_callback(self, fun):
        self._notify_mission_list_change_callback = fun

    def onRead(self, data):
        self._frame.setNewFrame(data)

    def login(self, seq, user_name, passwd):
        """登录"""
        md5 = hashlib.md5()
        md5.update(passwd.encode('utf8'))
        login_request = main_pb2.LoginRequest(username=user_name, password=md5.hexdigest())
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOGIN, login_request=login_request)

    def logout(self, seq):
        """登出"""
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOGOUT)

    def systemFunctions(self, seq, functions):
        """系统功能函数：详见functional_group函数"""
        function = self.systemfunctions.functional_group(functions)
        self._send_command_msg(seq, function)

    def setSpeedLevel(self,seq,level):
        """设置用户速度级别"""
        self._send_command_msg(seq, main_pb2.CMD_SET_SPEED_LEVEL,paramInt=level)

    def setSpeakerVolume(self,seq,volume):
        """设置语音模块声音大小"""
        self._send_command_msg(seq, main_pb2.CMD_SET_SPEAKER_VOLUME, paramInt=volume)

    def setManualSpeed(self,seq,speed):
        """设置手动SRC运动速度，确保处于 OPERATION_MANUAL 模式下"""
        self._send_command_msg(seq, main_pb2.CMD_SET_MANUAL_SPEED, paramInt=speed)

    def set_current_map(self, seq, map_name):
        """设置当前地图"""
        self._send_command_msg(seq, main_pb2.CMD_SET_CUR_MAP, paramStr=map_name)

    def switch_map(self, seq, map_name, station_no=0, pose=None, force_location=False):
        """切换地图"""
        self._send_command_msg(seq, main_pb2.CMD_MAP_SWITCHING, paramStr=map_name, paramInt=station_no, pose=pose,
                               param_boolean=force_location)
    def getAboutus(self, seq):
        """获取关于相关信息,软件版本等等"""
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_INFO)

    def getAllState(self,seq):
        """获取系统状态信息"""
        self._sendRequestMsg(seq, main_pb2.SystemState.SYS_STATE_TASK_NAV_WAITING_FINISH)

    def getSrosConfig(self, seq):
        """获取SROS配置参数"""
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOAD_CONFIG)

    def move_to_station(self, seq, no, station_id, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        """导航到站点"""
        movement_task = main_pb2.MovementTask(
            no=no,
            type=main_pb2.MovementTask.MT_MOVE_TO_STATION,
            stations=[station_id],
            avoid_policy=avoid_policy
        )

        self._send_command_msg(seq, main_pb2.CMD_NEW_MOVEMENT_TASK, movement_task=movement_task)

    def move_follow_path(self, seq, no, paths, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        """追加路径"""
        movement_task = main_pb2.MovementTask(
            no=no,
            type=main_pb2.MovementTask.MT_MOVE_FOLLOW_PATH,
            avoid_policy=avoid_policy
        )
        for path in paths:
            proto_path = movement_task.paths.add()
            proto_path.type = path.type.value
            proto_path.sx = path.sx
            proto_path.sy = path.sy
            proto_path.ex = path.ex
            proto_path.ey = path.ey
            proto_path.cx = path.cx
            proto_path.cy = path.cy
            proto_path.dx = path.dx
            proto_path.dy = path.dy
            proto_path.radius = path.radius
            proto_path.rotate_angle = path.rotate_angle
            proto_path.direction = path.direction.value
            proto_path.limit_v = path.limit_v
            proto_path.limit_w = path.limit_w
        self._send_command_msg(seq, main_pb2.CMD_NEW_MOVEMENT_TASK, movement_task=movement_task)

    def replace_move_path(self, seq, no, paths):
        proto_paths = []
        for path in paths:
            proto_path = main_pb2.Path()
            proto_path.type = path.type.value
            proto_path.sx = path.sx
            proto_path.sy = path.sy
            proto_path.ex = path.ex
            proto_path.ey = path.ey
            proto_path.cx = path.cx
            proto_path.cy = path.cy
            proto_path.dx = path.dx
            proto_path.dy = path.dy
            proto_path.radius = path.radius
            proto_path.rotate_angle = path.rotate_angle
            proto_path.direction = path.direction.value
            proto_path.limit_v = path.limit_v
            proto_path.limit_w = path.limit_w
            proto_paths.append(proto_path)
        self._send_command_msg(seq, main_pb2.CMD_SINGLE_PATH_REPLACE, paramInt=no, paths=proto_paths)

    def excute_action_task(self, seq, no, action_id, param0, param1):
        """动作运动函数"""
        action_task = main_pb2.ActionTask(
            no=no,
            id=action_id,
            param0=param0,
            param1=param1
        )
        self._send_command_msg(seq, main_pb2.CMD_NEW_ACTION_TASK, action_task=action_task)

    def readInputRegisters(self, seq, start_addr, count):
        """读取输入寄存器"""
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_READ_INPUT_REGISTER, param_int=start_addr, param_int1=count)

    def set_current_map(self, map_name):
        """设置当前地图"""
        self._send_command_msg(main_pb2.CMD_SET_CUR_MAP, paramStr=map_name)

    def start_location(self, seq):
        """开始定位"""
        self._send_command_msg(seq, main_pb2.CMD_START_LOCATION, paramBool=False)

    def set_initial_pose(self, seq, x, y, angle):
        """设置初始位姿"""
        pose = main_pb2.Pose(
            x=x,
            y=y,
            yaw=math.radians(angle) * 1000
        )
        self._send_command_msg(seq, main_pb2.CMD_SET_LOCATION_INITIAL_POSE, pose=pose)

    def _send_command_msg(self, seq, cmdType, paramInt=None, paramInt1=None, paramStr=None, pose=None, movement_task=None,
                          action_task=None, missionLst=None, lockerIP=None, lockerNickname=None, paths=None, paramBool=False):
        command = main_pb2.Command(
            command=cmdType,
            param_int=paramInt,
            param_int1=paramInt1,
            pose=pose,
            movement_task=movement_task,
            action_task=action_task,
            param_str=paramStr,
            mission_list=missionLst,
            locker_ip_address=lockerIP,
            locker_nickname=lockerNickname,
            paths=paths
        )
        message = main_pb2.Message(
            type=main_pb2.MSG_COMMAND,
            seq=seq,
            session_id=self._session_id,
            command=command)

        self._sendMsg(message)

    def _sendRequestMsg(self, seq, request_type, login_request=None, file_op=None, param_str=None, param_str1=None,
                        config=None, param_int=None, param_int1=None):
        request = main_pb2.Request(
            request_type=request_type,
            login_request=login_request,
            file_op=file_op,
            param_str=param_str,
            param_str1=param_str1,
            param_int=param_int,
            param_int1=param_int1,
            config=config)

        message = main_pb2.Message(
            type=main_pb2.MSG_REQUEST,
            seq=seq,
            session_id=self._session_id,
            request=request)

        self._sendMsg(message)

    def _send_response_msg(self, response_type, seq, notify_type):
        notification_response = main_pb2.NotifyResponse(
            ack=True,
            type=notify_type
        )
        response = main_pb2.Response(
            response_type=response_type,
            notify_response=notification_response
        )
        message = main_pb2.Message(
            type=main_pb2.MSG_RESPONSE,
            seq=seq,
            session_id=self._session_id,
            response=response)
        self._sendMsg(message)

    def _sendMsg(self, message):
        msg = message.SerializeToString()
        frame = srp_frame.Frame.buildFrame(msg)
        self._write(frame)

    def _handleRecvResponseMsg(self, msg):
        response = msg.response
        value = {}
        if response.result.result_state == main_pb2.ResponseResult.RESPONSE_OK or \
                response.result.result_state == main_pb2.ResponseResult.RESPONSE_PROCESSING:
            if response.response_type == main_pb2.Response.RESPONSE_LOGIN:
                self._session_id = msg.session_id
            elif response.response_type == main_pb2.Response.RESPONSE_LOAD_CONFIG:
                value = list(response.config)
            elif response.response_type == main_pb2.Response.RESPONSE_SYSTEM_STATE:
                system_state = response.system_state
                if self._system_state_callback is not None:
                    self._system_state_callback(system_state)
            elif response.response_type == main_pb2.Response.RESPONSE_HARDWARE_STATE:
                if self._hardware_state_callback:
                    self._hardware_state_callback(response.hardware_state)
            elif response.response_type == main_pb2.Response.RESPONSE_READ_INPUT_REGISTER:
                value = response.registers
            elif response.response_type == main_pb2.Response.RESPONSE_INFO:
                value = response.info
            self._response_callback(msg.seq, response.response_type, True, value=value)
        else:
            self._response_callback(msg.seq, response.response_type, False, result_code=response.result.result_code)

    def _ack_notification(self, message):
        if message.seq <= 0:
            return
        self._send_response_msg(main_pb2.Response.RESPONSE_NOTIFY, message.seq, message.notification.notify_type)

    def _handle_recv_notification_msg(self, notification):
        if notification.notify_type == main_pb2.Notification.NOTIFY_MOVE_TASK_FINISHED:
            if self._notify_move_task_finished_callback is not None:
                self._notify_move_task_finished_callback(notification)
        elif notification.notify_type == main_pb2.Notification.NOTIFY_ACTION_TASK_FINISHED:
            if self._notify_action_task_finished_callback is not None:
                self._notify_action_task_finished_callback(notification)
        elif notification.notify_type == main_pb2.Notification.NOTIFY_MISSION_LIST_CHANGED:
            if self._notify_mission_list_change_callback is not None:
                self._notify_mission_list_change_callback(notification.mission_list)
        else:
            pass

    def _onNewMessageCallback(self, msg):
        try:
            message = main_pb2.Message()
            message.ParseFromString(msg)
        except BaseException as e:
            log.error(e)
            raise e

        if message.type == main_pb2.MSG_RESPONSE:
            self._handleRecvResponseMsg(message)
        elif message.type == main_pb2.MSG_NOTIFICATION:
            self._ack_notification(message)
            self._handle_recv_notification_msg(message.notification)
        else:
            pass

    def is_last_action_state_running(self):
        return self._last_action_state == main_pb2.ActionTask.TaskState.AT_WAIT_FOR_START or \
        self._last_action_state == main_pb2.ActionTask.TaskState.AT_RUNNING or \
        self._last_action_state == main_pb2.ActionTask.TaskState.AT_PAUSED or \
        self._last_action_state == main_pb2.ActionTask.TaskState.AT_IN_CANCEL or \
        self._last_action_state == main_pb2.ActionTask.TaskState.AT_TASK_WAIT_FOR_ACK


class SystemFunctions():

    def functional_group(self, function):
        try:
            functions = {
                'CMD_RESET_SROS': 0x0F,  # 重启SROS
                'CMD_SRC_RESET': 0x08,  # 重启SRC
                'CMD_SRC_PAUSE': 0x03,  # 暂停SRC运动
                'CMD_SRC_CONTINUE': 0x04,  # 继续SRC运动
                'CMD_SRC_STOP': 0x05,  # 停止SRC运动
                'CMD_START_LOCATION': 0x01,  # 启动定位
                'CMD_STOP_LOCATION': 0x02,  # 停止定位
                'CMD_PAUSE_MOVEMENT': 0x03,  # 暂停运动
                'CMD_CONTINUE_MOVEMENT': 0x04,  # 恢复运动
                'CMD_STOP_MOVEMENT': 0x05,  # 停止运动
                'CMD_ENABLE_MANUAL_CONTROL': 0x06,  # 开启手动模式
                'CMD_DISABLE_MANUAL_CONTROL': 0x07,  # 关闭手动模式
                'CMD_ENABLE_OBSTACLE_AVOID': 0x0C,  # 启用避障
                'CMD_DISABLE_OBSTACLE_AVOID': 0x0D,  # 停用避障
                'CMD_STOP_SROS': 0x0E,  # 正常停止sros各模块
                'CMD_RESET_SROS': 0x0F,  # 重新启动sros各模块(包括src)
                'CMD_TRIGGER_EMERGENCY': 0x28,  # 触发急停
                'CMD_CANCEL_EMERGENCY': 0x12,  # 解除急停状态
                'CMD_ENTER_POWER_SAVE_MODE': 0x31,  # 进入低功耗模式
                'CMD_EXIT_POWER_SAVE_MODE': 0x32,  # 退出低功耗模式
                'CMD_ENABLE_AUTO_CHARGE': 0x13,  # 启动自动充电
                'CMD_STOP_CHARGE': 0x33,  # 停止充电
                'CMD_START_MISSION': 0x42,  # 开始mission
                'CMD_CANCEL_MISSION': 0x43,  # 取消mission
                'CMD_CONTINUE_MISSION': 0x45,  # 继续mission
                'CMD_REORDER_MISSION': 0x44,  # 恢复mission
                'CMD_ADD_PGV_INFO': 0x50,  # 记录当前pgv信息
                'CMD_DEL_PGV_INFO': 0x51,  # 删除当前pgv信息
                'CMD_NEW_MAP_START': 0x14,  # 开始绘ready_for_new_movement_task制新地图
                'CMD_NEW_MAP_STOP': 0x15,  # 结束绘制新地图（保存）
                'CMD_NEW_MAP_CANCEL': 0x16,  # 取消绘制新地图（不保存）
                'CMD_LOCK_CONTROL_MUTEX': 0x1A,  # 获取独占许可，获取成功后，其他用户将不能继续控制sros，只能监控sros
                'CMD_UNLOCK_CONTROL_MUTEX': 0x1B,  # 释放独占许可
                'CMD_FORCE_UNLOCK_CONTROL_MUTEX': 0x1C,  # 强制释放别人的独占许可(需要admin及其以上的权限）
                'CMD_CANCEL_MOVEMENT_TASK': 0x21,  # 取消移到任务
                'CMD_SET_CHECKPOINT': 0x35,  # 设置移动任务的关卡，用于交通管制，车辆会停止关卡前
                'CMD_ENABLE_AUTO_UPLOAD_LASER_POINT': 0x2A,  # 设置主动上传雷达点
                'CMD_DISABLE_AUTO_UPLOAD_LASER_POINT': 0x2B,  # 设置不主动上传雷达点
                'CMD_ENABLE_UPLOAD_AVOID_OBSTACLE_PREDICTION': 0x38,  # 设置主动上传避障预测信息（该信息带宽占用多）
                'CMD_DISABLE_UPLOAD_AVOID_OBSTACLE_PREDICTION': 0x39,  # 设置不主动上传避障预测信息
                # 启用调试信息模式，会上传打开一下调试信息，这些信息的的获取占用很多资源，只有调试的时候才需要，其他正常运行都不需要.
                # 如：开启下视PGV值实时显示，这个只有调试的时候要用到，这个开启需要占用大量CPU
                'CMD_ENABLE_DEBUG_INFO': 0x54,  # 开启调试模式
                'CMD_DISABLE_DEBUG_INFO': 0x55,  # 关闭调试模式
                'CMD_RESET_FAULT': 0x2C,  # 尝试复位故障
            }
            return functions[str(function)]
        except BaseException as e:
            print('functional_group ERROR:', e)