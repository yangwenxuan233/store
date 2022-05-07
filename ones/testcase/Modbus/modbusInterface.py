#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ywx
# @Time: 2022/4/19 11:20


import time

from packages.caseResult import CaseResult
from packages.logControl import Logging
from packages.yamlControl import getYamlData
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class TestCase(object):

    def __init__(self, parameter):
        """
        本类是Matrix API对外接口测试用例
        参考: https://standard-robots.yuque.com/sn973i/dtv5kk/mg2y8d
        :param parameter:传入参数
        """
        self.parameter = parameter
        self.result = CaseResult(parameter['task_uuid'])
        self.logger = Logging('modbusInterface')
        self.ip = parameter['AGV_IP']
        self._client = None

    def pymodbus_connect_tcp(self):
        """
        pymodbus client TCP方式连接AGV
        :return:
        """
        try:
            self._client = ModbusTcpClient(self.ip, port=502, timeout=10)
            try:
                ret = self._client.connect()
            except BaseException:
                return False
            if ret:
                return True
            else:
                return False
        except BaseException as e:
            self.logger.error('pymodbus_connect_tcp :' + str(e))

    def case6826(self):
        """
        title: 使用异常状态车辆的IP连接
        :return:
        """
        try:
            self.ip = '123.28.10.19'
            ret = self.pymodbus_connect_tcp()
            if ret:
                self._client.close()
                return self.result.caseResult('failed', f'case6826: pymodbus connect succeeded, {ret}')
            else:
                self._client.close()
                return self.result.caseResult('passed', 'case6826: pymodbus connect failed')
        except BaseException as e:
            self._client.close()
            return self.result.caseResult('failed', f'case6826:{e}')

    def case6827(self):
        """
        title: 使用正常通讯的车辆IP连接
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                return self.result.caseResult('passed', f'case6827: pymodbus connect succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case6827: pymodbus connect failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case6827:{e}')

    def case5297(self):
        """
        title: 触发急停
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(7, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5297: trigger crash-stop succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5297: trigger crash-stop failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5297:{e}')

    def case5289(self):
        """
        title: DO 0 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(33, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5289: write DO 0 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5289: write DO 0 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5289:{e}')

    def case5290(self):
        """
        title: DO 1 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(34, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5290: write DO 1 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5290: write DO 1 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5290:{e}')

    def case5291(self):
        """
        title: DO 2 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(35, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5291: write DO 2 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5291: write DO 2 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5291:{e}')

    def case5292(self):
        """
        title: DO 3 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(36, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5292: write DO 3 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5292: write DO 3 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5292:{e}')

    def case5293(self):
        """
        title: DO 4 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(37, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5293: write DO 4 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5293: write DO 4 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5293:{e}')

    def case5294(self):
        """
        title: DO 5 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(38, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5294: write DO 5 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5294: write DO 5 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5294:{e}')

    def case5295(self):
        """
        title: DO 6 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(39, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5295: write DO 6 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5295: write DO 6 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5295:{e}')

    def case5296(self):
        """
        title: DO 7 写入0xFF00使能
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(40, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5296: write DO 7 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5296: write DO 7 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5296:{e}')

    def case5298(self):
        """
        title: 放行，即:发送此信号动作(131,0,0)会结束
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(49, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5298: release succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5298: release failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5298:{e}')

    def case5299(self):
        """
        title: 继续mission任务
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(97, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5299: continue mission succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5299: continue mission failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5299:{e}')

    def case5300(self):
        """
        title: 继续运动
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(2, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5300: continue moving succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5300: continue moving failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5300:{e}')

    def case5301(self):
        """
        title: 解除急停
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(8, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5301: release crash-stop succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5301: release crash-stop failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5301:{e}')

    def case5302(self):
        """
        title: 进入低功耗模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(11, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5302: enter low-power consumption mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5302: enter low-power consumption mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5302:{e}')

    def case5303(self):
        """
        title: 进入调度模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(51, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5303: enter scheduling mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5303: enter scheduling mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5303:{e}')

    def case5304(self):
        """
        title: 开启屏蔽避障区域
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(6, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5304: open shielding obstacle area succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5304: open shielding obstacle area failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5304:{e}')

    def case5305(self):
        """
        title: 启动充电
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(9, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5305: open charge succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5305: open charge failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5305:{e}')

    def case5306(self):
        """
        title: 启动手动控制
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(15, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5306: open manual control succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5306: open manual control failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5306:{e}')

    def case5307(self):
        """
        title: 取消mission任务
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(99, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5307: cancel mission succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5307: cancel mission control failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5307:{e}')

    def case5308(self):
        """
        title: 停止充电
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(10, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5308: stop charging succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5308: stop charging failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5308:{e}')

    def case5309(self):
        """
        title: 停止定位
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(5, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5309: stop locating succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5309: stop locating failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5309:{e}')

    def case5310(self):
        """
        title: 停止手动控制
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(16, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5310: stop manual control succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5310: stop manual control failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5310:{e}')

    def case5311(self):
        """
        title: 停止运动
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(3, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5311: stop moving succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5311: stop moving failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5311:{e}')

    def case5312(self):
        """
        title: 退出低功耗模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(12, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5312: quit low-power consumption mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5312: quit low-power consumption mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5312:{e}')

    def case5313(self):
        """
        title: 退出调度模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(51, 0x0000, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5313:  quit scheduling mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5313:  quit scheduling mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5313:{e}')

    def case5314(self):
        """
        title: 退出屏蔽避障区域
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(51, 0x0000, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5314: open shielding obstacle area succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5314: open shielding obstacle area failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5314:{e}')

    def case5315(self):
        """
        title: 重启SROS
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(14, 0xFF00, unit=17)
                time.sleep(30)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5315: reboot SROS succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5315: reboot SROS failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5315:{e}')

    def case5316(self):
        """
        title: 以0.389rad/s向右旋转(每设置一次移动100ms)
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(20, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5316: 0.389rad/s turn right succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5316: 0.389rad/s turn right failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5316:{e}')

    def case5317(self):
        """
        title: 以0.389rad/s向右旋转(每设置一次移动100ms)
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(19, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5317: 0.389rad/s turn left succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5317: 0.389rad/s turn left failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5317:{e}')

    def case5318(self):
        """
        title: 以0.495m/s向后移动(每设置一次移动100ms)
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(18, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5318: 0.495m/s move backward succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5318: 0.495m/s move backward failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5318:{e}')

    def case5319(self):
        """
        title: 以0.495m/s向前移动(每设置一次移动100ms)
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(17, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5319: 0.495m/s move forward succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5319: 0.495m/s move forward failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5319:{e}')

    def case5320(self):
        """
        title: 暂停mission任务
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(97, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5320: stop mission succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5320: stop mission failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5320:{e}')

    def case5321(self):
        """
        title: 暂停mission任务
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                ret = self._client.write_coil(1, 0xFF00, unit=17)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5321: stop moving succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5321: stop moving failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5321:{e}')

    def case5322(self):
        """
        title: DI 0
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10017, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5322: read DI 0 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5322: read DI 0 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5322:{e}')

    def case5323(self):
        """
        title: DI 1
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10018, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5323: read DI 1 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5323: read DI 1 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5323:{e}')

    def case5324(self):
        """
        title: DI 2
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10019, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5324: read DI 2 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5324: read DI 2 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5324:{e}')

    def case5325(self):
        """
        title: DI 3
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10020, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5325: read DI 3 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5325: read DI 3 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5325:{e}')

    def case5326(self):
        """
        title: DI 4
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10021, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5326: read DI 4 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5326: read DI 4 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5326:{e}')

    def case5327(self):
        """
        title: DI 5
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10022, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5327: read DI 5 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5327: read DI 5 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5327:{e}')

    def case5328(self):
        """
        title: DI 6
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10023, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5328: read DI 6 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5328: read DI 6 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5328:{e}')

    def case5329(self):
        """
        title: DI 7
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10024, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5329: read DI 7 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5329: read DI 7 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5329:{e}')

    def case5330(self):
        """
        title: DO 0
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10033, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5330: read DO 0 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5330: read DO 0 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5330:{e}')

    def case5331(self):
        """
        title: DO 1
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10034, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5331: read DO 1 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5331: read DO 1 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5331:{e}')

    def case5332(self):
        """
        title: DO 2
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10035, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5332: read DO 2 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5332: read DO 2 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5332:{e}')

    def case5333(self):
        """
        title: DO 3
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10036, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5333: read DO 3 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5333: read DO 3 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5333:{e}')

    def case5334(self):
        """
        title: DO 4
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10037, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5334: read DO 4 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5334: read DO 4 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5334:{e}')

    def case5335(self):
        """
        title: DO 5
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10038, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5335: read DO 5 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5335: read DO 5 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5335:{e}')

    def case5336(self):
        """
        title: DO 6
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10039, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5336: read DO 6 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5336: read DO 6 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5336:{e}')

    def case5337(self):
        """
        title: DO 7
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10040, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5337: read DO 7 succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5337: read DO 7 failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5337:{e}')

    def case5338(self):
        """
        title: 当前是否可以运行移动任务
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10009, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5338: read whether can run move task succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5338: read whether can run move task failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5338:{e}')

    def case5339(self):
        """
        title: 放行, 即: 动作(131,0,0)会等待此信号
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10049, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5339: read release succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5339: read release failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5339:{e}')

    def case5340(self):
        """
        title: 急停是否触发
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10001, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5340: read whether can trigger crash-stop succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5340: read whether can trigger crash-stop failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5340:{e}')

    def case5341(self):
        """
        title: 急停是否可恢复
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10002, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5341: read whether can release crash-stop succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5341: read whether can release crash-stop failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5341:{e}')

    def case5342(self):
        """
        title: 是否抱闸
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10003, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5342: read whether open brake succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5342: read whether open brake failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5342:{e}')

    def case5343(self):
        """
        title: 是否处于低功耗模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10005, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5343: read whether in low-power consumption mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5343: read whether in low-power consumption mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5343:{e}')

    def case5344(self):
        """
        title: 是否处于调度模式
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10051, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5344: read whether in scheduling mode succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5344: read whether in scheduling mode failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5344:{e}')

    def case5345(self):
        """
        title: 是否遇到障碍物减速
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10006, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5345: read whether obstacles to slow succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5345: read whether obstacles to slow failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5345:{e}')

    def case5346(self):
        """
        title: 是否遇到障碍物暂停
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10007, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5346: read whether obstacles to stop succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5346: read whether obstacles to stop failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5346:{e}')

    def case5347(self):
        """
        title: 是否正在充电
        :return:
        """
        try:
            ret = self.pymodbus_connect_tcp()
            if ret:
                result = self._client.read_discrete_inputs(10004, unit=17)
                ret = result.getBit(0)
                self.logger.info(ret)
                return self.result.caseResult('passed', f'case5346: read whether charging succeeded, {ret}')
            else:
                return self.result.caseResult('failed', 'case5346: read whether charging failed')
        except BaseException as e:
            return self.result.caseResult('failed', f'case5346:{e}')
