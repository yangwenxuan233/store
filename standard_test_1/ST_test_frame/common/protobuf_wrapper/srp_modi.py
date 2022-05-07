#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file srp.py
# author pengjiali
# date 19-6-19.
# copyright Copyright (c) 2019 Standard Robots Co., Ltd. All rights reserved.
# describe 与sros进行protobuf通信的封装

import asyncio
import threading
import srp_protobuf
import main_pb2
from async_result import AsyncResult, AsyncResultState
from concurrent import futures
import socket

from protobuf_wrapper.log import log


# client
class SrpProtocol(asyncio.Protocol):
    def __init__(self, srp):
        self._srp = srp

    def connection_made(self, transport):
        self._srp.connection_made(transport)

    def data_received(self, data):
        self._srp.data_received(data)

    def error_received(self, exc):
        self._srp.error_received(exc)

    def connection_lost(self, exc):
        self._srp.connection_lost(exc)


class SRP:
    """
    @describe:  本类用来和sros通信
                本类内部有一个线程用于处理protobuf协议的解析、收发，本类是线程安全的
                本类的方法既支持同步通信的方式也支持异步通信的方式，同步通信的方式主要用来测试，比如连续发送task而不等回复
                默认为异步函数，同步函数前面都加了前缀:sync_,和node.js的库命名规范类似
    @NOTE: 异步调用时，假定不会同时调用， 现在只有一个AsyncResult类来阻塞等待sros的响应
    """

    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._transport = None
        self._protocl = None
        self._protobuf = srp_protobuf.SrpProtobuf(self.write_callback, self.response_callback)
        self._protobuf.set_notify_move_task_finished_callback(self.on_move_task_finish)
        self._protobuf.set_notify_action_task_finished_callback(self.on_action_task_finish)
        self._seq = 0
        self._wait_seq = 0  # 等待回复的seq
        self._sync_result = AsyncResult(self._loop)

        # 同步等待任务（动作）执行结束
        self._sync_task_result = AsyncResult(self._loop)

        self._callback_connect_changed = None
        self._callback_move_task_finish = None
        self._callback_action_task_finish = None

        # def start_loop(loop):
        #     asyncio.set_event_loop(loop)
        #     loop.run_forever()
        #
        # t = threading.Thread(target=start_loop, args=(self._loop,))
        # t.start()

    def set_callback_connect(self, fun):
        self._callback_connect_changed = fun

    def set_system_state_callback(self, fun):
        self._protobuf.set_system_state_callback(fun)

    def set_hardware_state_callback(self, fun):
        self._protobuf.set_hardware_state_callback(fun)

    def set_laser_point_callback(self, fun):
        self._protobuf.set_laser_point_callback(fun)

    def set_notify_move_task_finished_callback(self, fun):
        self._callback_move_task_finish = fun

    def set_notify_action_task_finished_callback(self, fun):
        self._callback_action_task_finish = fun

    def set_notify_mission_list_change_callback(self, fun):
        self._protobuf.set_notify_mission_list_change_callback(fun)

    def on_move_task_finish(self, notification):
        if self._callback_move_task_finish:
            self._callback_move_task_finish(notification.movement_task)

    def on_action_task_finish(self, notification):
        # 不用判断wait_seq，因为在执行动作后可能进行了其他操作
        action_task = notification.action_task
        result = action_task.result
        err_code = action_task.result_code
        log.info("on action task finish %d %d" % (result, err_code))
        if result == main_pb2.TASK_RESULT_OK or result == main_pb2.TASK_RESULT_CANCELED:
            self._sync_task_result.accept(result, action_task.result_str)
        else:
            self._sync_task_result.reject(err_code)
        if self._callback_action_task_finish:
            self._callback_action_task_finish(action_task)

    def _connect(self, ip_addr):
        '''
        由于同样的ip和port链接sros经常出问题，所以此处一直用端口号为8888的端口号链接sros
        :param ip_addr:
        :return:
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            SOURCE_PORT = 8888
            sock.bind(('0.0.0.0', SOURCE_PORT))
            sock.connect((ip_addr, 5001))
            self._transport, self._protocl = await self._loop.create_connection(lambda: SrpProtocol(self), sock=sock)
            return True
        except BaseException as e:
            log.error("Connect to sros failed:")
            log.error(e)
        return False



################################################################################
################################################################################
    # 一下为异步指令
    def login(self, ip_addr, user_name, passwd):
        '''
        登录sros
        :param ip_addr: target sros's ip address
        :param user_name: clear text
        :param passwd: clear text
        :return: none
        '''
        f = asyncio.run_coroutine_threadsafe(self._connect(ip_addr), self._loop)
        result = f.result(3)
        if not result:
            return False
        log.info('Connect succeed ip:' + ip_addr + 'port:' + str(5001))

        try:
            self._run_sync_threadsafe(self._protobuf.login, user_name, passwd)
            if self._callback_connect_changed:
                self._callback_connect_changed(True)
            return True
        except BaseException as e:
            log.error("Login sros failed: ")
            log.error(e)
        return False

    def logout(self):
        try:
            self._run_sync_threadsafe(self._protobuf.logout)
        except BaseException as e:
            log.error(e)
        if self._transport:
            self._transport.close()

        if self._callback_connect_changed:
            self._callback_connect_changed(False)

    def get_sros_config(self, key):
        configs = self._run_sync_threadsafe(self._protobuf.get_sros_config)
        for config in configs:
            if config.key == key:
                return config.value
        return None

    def get_info(self):
        info = self._run_sync_threadsafe(self._protobuf.get_info)
        return info

    def triger_emergency(self):
        self._run_sync_threadsafe(self._protobuf.setEmergency)

    def cancel_emergency(self):
        self._run_sync_threadsafe(self._protobuf.cancelEmergencyState)

    def move_to_station(self, no, station_id, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        self._run_sync_threadsafe(self._protobuf.move_to_station, no, station_id, avoid_policy)

    def move_follow_path(self, no, paths, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        self._run_sync_threadsafe(self._protobuf.move_follow_path, no, paths, avoid_policy)

    # 追加路径
    def replace_move_path(self, no, paths):
        self._run_sync_threadsafe(self._protobuf.replace_move_path, no, paths)

    def pause_task(self):
        self._run_sync_threadsafe(self._protobuf.pause_task)

    def continue_task(self):
        self._run_sync_threadsafe(self._protobuf.continue_task)

    def cancel_task(self):
        self._run_sync_threadsafe(self._protobuf.cancel_task)

    def cancel_movement_task(self):
        self._run_sync_threadsafe(self._protobuf.cancel_movement_task)

    def set_current_map(self, map_name):
        self._run_sync_threadsafe(self._protobuf.set_current_map, map_name)

    def start_location(self, x, y, angle):
        self._run_sync_threadsafe(self._protobuf.set_initial_pose, x, y, angle)
        self._run_sync_threadsafe(self._protobuf.start_location, timeout=15)

    def start_charge(self, no):
        log.info("Start charge")
        self.async_excute_action_task(no, 78, 1, 0)

    def stop_charge(self, no):
        log.info("Stop charge")
        self.async_excute_action_task(no, 78, 2, 0)

    # 同步执行，直到动作结果返回或超时
    def excute_action_task(self, no, action_id, param0, param1):
        log.info("Execute action " + str(action_id) + " " + str(param0) + " " + str(param1))
        result = self._run_sync_task_threadsafe(self._protobuf.excute_action_task, no, action_id, param0, param1)
        return result

    def cancel_action_task(self):
        self._run_sync_threadsafe(self._protobuf.cancel_action_task)

    def read_input_registers(self, start_addr, count):
        return self._run_sync_threadsafe(self._protobuf.readInputRegisters, start_addr, count)

    # 以下为异步步指令
    def async_move_to_station(self, no, station_id, avoid_policy=main_pb2.MovementTask.OBSTACLE_AVOID_WAIT):
        self._run_async_threadsafe(self._protobuf.move_to_station, no, station_id, avoid_policy)

    def async_excute_action_task(self, no, action_id, param0, param1):
        self._run_async_threadsafe(self._protobuf.excute_action_task, no, action_id, param0, param1)

    def _run_sync_threadsafe(self, fun, *args, timeout=3):
        f = asyncio.run_coroutine_threadsafe(self._sync_request(fun, *args), self._loop)
        return f.result(timeout)
        # to_do.append(f)
        # return f.result()会阻塞主线程
        # for future in futures.as_completed(to_do, timeout):
        #     return future.result()

    # 移动动作任务同步执行直到返回结果
    def _run_sync_task_threadsafe(self, fun, *args, timeout=10 * 60):
        # to_do = []
        f = asyncio.run_coroutine_threadsafe(self._sync_task(fun, *args), self._loop)
        return f.result(timeout)
        # to_do.append(f)
        # # return f.result()会阻塞主线程
        # for future in futures.as_completed(to_do, timeout):
        #     return future.result()

    async def _sync_request(self, fun, *args):
        self._seq += 1
        self._wait_seq = self._seq
        self._sync_result.clear()
        fun(self._seq, *args)
        return await self._sync_result.wait()

    async def _sync_task(self, fun, *args):
        self._seq += 1
        self._wait_seq = self._seq
        self._sync_task_result.clear()
        fun(self._seq, *args)
        return await self._sync_task_result.wait()

    def _run_async_threadsafe(self, fun, *args):
        self._loop.call_soon_threadsafe(self._async_request, fun, *args)

    def _async_request(self, fun, *args):
        self._seq += 1
        # self._wait_seq = self._seq
        fun(self._seq, *args)

    async def _connect(self, ip_addr):
        '''
        由于同样的ip和port链接sros经常出问题，所以此处一直用端口号为8888的端口号链接sros
        :param ip_addr:
        :return:
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            SOURCE_PORT = 8888
            sock.bind(('0.0.0.0', SOURCE_PORT))
            sock.connect((ip_addr, 5001))
            self._transport, self._protocl = await self._loop.create_connection(lambda: SrpProtocol(self), sock=sock)
            return True
        except BaseException as e:
            log.error("Connect to sros failed:")
            log.error(e)
        return False

    def connection_made(self, transport):
        log.info('connected!')

    def data_received(self, data):
        self._protobuf.onRead(data)

    def error_received(self, exc):
        log.error('Error received:' + str(exc))

    def connection_lost(self, exc):
        log.warning("Socket closed: " + str(exc))
        self.logout()

    def write_callback(self, data):
        self._transport.write(data)

    def response_callback(self, seq, response_type, ok, value=None, result_code=None):
        if seq == self._wait_seq:
            if ok:
                self._sync_result.accept(value)
            else:
                self._sync_result.reject(result_code)

    def get_result_code(self):
        return self._sync_result.get_result()

    def get_result_dat(self):
        return self._sync_task_result.get_result_dat()


if __name__ == '__main__':
    srp = SRP()
    srp.login('192.168.33.119', 'admin', 'admin')
    # srp.triger_emergency()
    # srp.cancel_emergency()
    print(srp.get_info())
    # try:
    #     srp.login('192.168.33.119', 'admin', 'admin')
    #     # srp.triger_emergency()
    #     # srp.cancel_emergency()
    #     print(srp.get_info())
    #     # print(srp.get_sros_config())
    #     # for i in range(1, 3):
    #     #     srp.move_to_station(1, i)
    # except BaseException as e:
    #     log.error(e)

    # for i in range(2, 50):
    #     srp.sync_move_to_station(i, 1)
