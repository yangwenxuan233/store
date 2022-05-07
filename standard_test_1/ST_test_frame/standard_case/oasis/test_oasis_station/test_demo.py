# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: testcase demo
"""

import datetime
import os
import unittest

import ddt
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings


@ddt.ddt
class TestDemo(unittest.TestCase):
    '''demo Testcase
    '''

    def setUp(self) -> None:
        '''用例初始化, 开启日志模块。
        '''
        self.logger = Logs()

    def tearDown(self) -> None:
        '''用例结束处理, 清除日志模块句柄。
        '''
        self.logger.logger.handlers.pop()

    def connect_agv(self):
        '''modbus_tcp连接。
        '''
        self.MASTER = modbus_tcp.TcpMaster(host=self.AGV_IP, port=502)
        self.MASTER.set_timeout(30)
        self.LOGGER.info("connected")

    def connection_status(self) -> None:
        """检测当前ip地址连接状态。
        畅通时直接返回, 反之则记录当前时间和日志信息。
        param: ip: ip地址
        return: None
        """
        while True:
            backinfo = os.popen(f"ping -w 1 {self.AGV_IP}").read()
            detil = str(backinfo).split('\n')
            if str(backinfo).find("回复") == -1:
                # 记录时间和返回值
                self.logger.info(str(datetime.datetime.now()) + "--" + str(self.AGV_IP) + "\n"
                                 + detil[2] + "\n" + detil[-2] + "\n")
            else:
                return

    @ddt.file_data(settings.BOARD_YAML)
    def test_param_allright(self, **kwargs):
        self.AGV_IP = kwargs['ip']
        try:
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
        except Exception as e:
            print(" " + str(e))
            self.connection_status()  # 断网重连
            self.connect_agv()
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取

        if NavStatus[0] == 2 and NavStatus[1] == 3:
            print('AGV状态正常')

        for i in range(30):
            self.station = 1
            print('前往目标站点', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                print(" " + str(e))
            while True:
                self.connection_status()  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                    self.connection_status()  # 断网重连
                    self.connect_agv()
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                finally:
                    self.connection_status()  # 断网重连
                    self.connect_agv()
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    break

            self.station = 2
            print('前往目标站点', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                print(" " + str(e))

            while True:
                self.connection_status()  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                    self.connection_status()  # 断网重连
                    self.connect_agv()
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                finally:
                    self.connection_status()  # 断网重连
                    self.connect_agv()
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    break
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
