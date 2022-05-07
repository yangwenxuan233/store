#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file srp_protobuf.py
# author pengjiali
# date 19-6-25.
# copyright Copyright (c) 2019 Standard Robots Co., Ltd. All rights reserved.
# describe

import hashlib
import main_pb2
import math
import frame as srp_frame

from protobuf_wrapper.log import log


class SrpProtobuf:

    def __init__(self, write_callback, response_callback):
        """
        本类处理protobuf协议的解析
        """
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
        # 设置新数据帧
        self._frame.setNewFrame(data)

    def login(self, seq, user_name, passwd):
        md5 = hashlib.md5()
        md5.update(passwd.encode('utf8'))

        login_request = main_pb2.LoginRequest(username=user_name, password=md5.hexdigest())
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOGIN, login_request=login_request)

    def logout(self, seq):
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOGOUT)

    def get_info(self, seq):
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_INFO)

    def get_sros_config(self, seq):
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_LOAD_CONFIG)

    def setEmergency(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_TRIGGER_EMERGENCY)

    def resetSROS(self, seq):
        # CMD_RESET_SRP
        self._send_command_msg(seq, main_pb2.CMD_RESET_SRP)

    def cancelEmergencyState(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_CANCEL_EMERGENCY)

    def set_manual_control(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_ENABLE_MANUAL_CONTROL)

    def disable_manual_control(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_DISABLE_MANUAL_CONTROL)

    def start_charge(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_ENABLE_AUTO_CHARGE)

    def stop_charge(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_STOP_CHARGE)

    def move_to_station(self, seq, no, station_id, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        movement_task = main_pb2.MovementTask(
            no=no,
            type=main_pb2.MovementTask.MT_MOVE_TO_STATION,
            stations=[station_id],
            avoid_policy=avoid_policy
        )

        self._send_command_msg(seq, main_pb2.CMD_NEW_MOVEMENT_TASK, movement_task=movement_task)

    def move_follow_path(self, seq, no, paths, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        log.info("Move follow path, task no %d" % no)
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

    # 追加路径，以支持发送多段路径时移动连续
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

    def pause_task(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_PAUSE_MOVEMENT)

    def continue_task(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_CONTINUE_MOVEMENT)

    def cancel_task(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_COMMON_CANCEL)

    def cancel_movement_task(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_CANCEL_MOVEMENT_TASK)

    def excute_action_task(self, seq, no, action_id, param0, param1):
        log.info("execute action no %d " % no)
        action_task = main_pb2.ActionTask(
            no=no,
            id=action_id,
            param0=param0,
            param1=param1
        )
        self._send_command_msg(seq, main_pb2.CMD_NEW_ACTION_TASK, action_task=action_task)

    def cancel_action_task(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_CANCEL_ACTION_TASK)

    def readInputRegisters(self, seq, start_addr, count):
        self._sendRequestMsg(seq, main_pb2.Request.REQUEST_READ_INPUT_REGISTER, param_int=start_addr, param_int1=count)

    def stop_location(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_STOP_LOCATION)

    def set_current_map(self, seq, map_name):
        self._send_command_msg(seq, main_pb2.CMD_SET_CUR_MAP, paramStr=map_name)

    def start_location(self, seq):
        self._send_command_msg(seq, main_pb2.CMD_START_LOCATION, paramBool=False)

    def set_initial_pose(self, seq, x, y, angle):
        pose = main_pb2.Pose(
            x=x,
            y=y,
            yaw=math.radians(angle) * 1000
        )
        self._send_command_msg(seq, main_pb2.CMD_SET_LOCATION_INITIAL_POSE, pose=pose)

    def _send_command_msg(self, seq, cmdType, paramInt=None, paramInt1=None, paramStr=None, pose=None,
                          movement_task=None,
                          action_task=None, missionLst=None, lockerIP=None, lockerNickname=None, paths=None,
                          paramBool=False):
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
        # 序列化
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
                # action_task = system_state.action_state
                # cur_state = action_task.state
                # if cur_state == main_pb2.ActionTask.TaskState.AT_FINISHED and self.is_last_action_state_running():
                #     if self._notify_action_task_finished_callback:
                #         self._notify_action_task_finished_callback(action_task)
                # self._last_action_state = cur_state
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
        log.info("on notify message: %d " % notification.notify_type)
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
            log.error('UNRACHABLE! notify type: ', notification.notify_type)
            # raise RuntimeError('UNRACHABLE! notify type: ', notification.notify_type)

    def _onNewMessageCallback(self, msg):
        try:
            message = main_pb2.Message()
            # 将message解包，反序列成
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
            log.error('UNREACHABLE! ' + str(message.type))
            # raise Exception('UNREACHABLE! ' + str(message.type))

    def is_last_action_state_running(self):
        return self._last_action_state == main_pb2.ActionTask.TaskState.AT_WAIT_FOR_START or \
               self._last_action_state == main_pb2.ActionTask.TaskState.AT_RUNNING or \
               self._last_action_state == main_pb2.ActionTask.TaskState.AT_PAUSED or \
               self._last_action_state == main_pb2.ActionTask.TaskState.AT_IN_CANCEL or \
               self._last_action_state == main_pb2.ActionTask.TaskState.AT_TASK_WAIT_FOR_ACK


if __name__ == '__main__':
    message = main_pb2.Message()
    try:
        # protobuf解包操作 序列消息解析为当前消息
        message.ParseFromString(bytes.fromhex('080015cc0a0000191a931dfe6b01000022020811'))  # fromhex：将hexstr转为：bytes
    except BaseException as e:
        log.error(e)
    print(message)
    log.info(message)
