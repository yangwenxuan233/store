import datetime
import json
import logging
import os
import socket
import struct
import time
import xlwt
import unittest

import modbus_tk.defines as cst
import paramiko
from modbus_tk import modbus_tcp

import Standard_Matrix_HTTP_API
import Standard_Modbus_Api


class TestStation(unittest.TestCase):
    '''Oasis站点精度用例, 直线站点精度-空载前进。
    '''

    def setUp(self) -> None:
        '''参数初始化, 开启日志。
        '''
        self.AGV_IP = '192.168.33.21'  # agv ip地址
        self.PGV_IP = '192.168.33.12'  # pgv ip地址
        self.speed = 300  # 最大线速度 单位mm/s
        self.acc_down = 100  # 减速度 单位mm/s²
        self.start_station = 1  # 测试起始站点
        self.target_station = 2  # 测试目标站点
        self.output_path = ''  # 结果输出路径
        self.times = 20  # 用例执行次数
        self.logger = logging.getLogger('station-straight-forward-nonload')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(ch)
        self.logger.info('用例执行: nonload-0.3-0.1')
        self.connect_agv()

    def tearDown(self) -> None:
        '''用例结束处理。
        '''
        return super().tearDown()

    def connect_agv(self):
        '''modbus_tcp连接。
        '''
        self.MASTER = modbus_tcp.TcpMaster(host=self.AGV_IP, port=502)
        self.MASTER.set_timeout(30)
        self.logger.info("connected")

    def test_main(self):
        '''用例分类: 直线站点精度-空载前进, 用例标题: 空载、速度0.3m/s、减速度0.1m/s²、直线前进,
        预期结果: 站点精度 < ±10mmm 偏角 < ±0.5°
        '''

    def param_setting(self) -> None:
        '''配置速度级别和减速度, 自动重启系统。
        '''
        # 配置速度级别
        matrix = Standard_Matrix_HTTP_API.SR_Matrix_HTTP(self.AGV_IP)
        matrix.modify_single_parameter(5301, {'value': self.speed})
        # 配置减速度
        matrix.modify_single_parameter(5304, {'value': self.acc_down})
        # 开启modbus_tcp
        matrix.modify_single_parameter(2101, {'value': 'True'})
        # 重启SROS
        ssh = paramiko.SSHClient()  # 创建ssh对象ko
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts中的主机
        ssh.connect(hostname=self.AGV_IP, port=2222, username='root', password='SRpasswd@2017')  # 建立连接
        stdin, stdout, stderr = ssh.exec_command('systemctl restart sros')  # 重启sros服务
        self.logger.info('正在重启SROS')
        time.sleep(20)
        # 解除重启后软急停状态
        modbus = Standard_Modbus_Api.SRPymodbus(self.AGV_IP)
        result = modbus.read_discrete_inputs(10001)
        print(result)
        modbus.write_single_coil_function('解除急停')
        time.sleep(2)
        result = modbus.read_discrete_inputs(10001)
        print(result)
        if not result:
            self.logger.info('解除急停成功')
        else:
            self.logger.error('解除急停异常')
        # 检查参数状态
        speed = int(dict(json.loads(matrix.get_single_config_parameter(973)))['value'])
        acc_down = int(dict(json.loads(matrix.get_single_config_parameter(5304)))['value'])
        if self.speed == speed and self.acc_down == acc_down:
            self.logger.info('参数设置成功, 当前最大线速度:', self.speed, ' 当前减速度:', self.acc_down)
            return
        else:
            self.logger.error('参数设置异常')

    def connection_status(ip: str) -> None:
        """检测当前ip地址连接状态。
        畅通时直接返回, 反之则记录当前时间和日志信息。
        param: ip: ip地址
        return: None
        """
        while True:
            backinfo = os.popen(f"ping -w 1 {ip}").read()
            detil = str(backinfo).split('\n')
            if str(backinfo).find("回复") == -1:
                # 记录时间和返回值
                with open("log.txt", "a+") as f:
                    f.write(str(datetime.datetime.now()) + "--" + str(ip) + "\n"
                            + detil[2] + "\n" + detil[-2] + "\n")
                    f.close()
                time.sleep(1)
            else:
                return

    def test_straight_forward_nonload(self):
        '''用例分裂: 直线站点精度-空载前进, 用例标题: 空载、速度0.3m/s、减速度0.1m/s²、直线前进,
        预期结果: 站点精度 < ±10mm, 偏角 < ±0.5°
        '''
        # 读取系统状态码
        self.connection_status(self.AGV_IP)  # 检查链接状态
        try:
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
        except Exception as e:
            print(" " + str(e))
            self.connection_status(self.AGV_IP)  # 断网重连
            self.connect_agv()
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
        finally:
            self.connection_status(self.AGV_IP)  # 断网重连
            self.connect_agv()
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
        if NavStatus[0] == 2 and NavStatus[1] == 3:
            self.logger.info('AGV状态正常')
            # 导航至起始站点
            self.connection_status(self.AGV_IP)
            self.logger.info('前往起始站点 ', self.start_station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.start_station])
            except Exception as e:
                self.logger.info(" " + str(e))
            while True:
                self.connection_status(self.AGV_IP)  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    # AGV状态正常，新建文件
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S.%f')
                    # 文件命名
                    XlsName = 'straight_forward_nonload' + '-' + str(self.AGV_IP) + "_" + str(now_time)\
                              + "_" + str(self.speed) + "_" + str(self.acc_down) + ".xls"
                    workBook = xlwt.Workbook()  # built xls
                    # 创建对应站点数据sheet
                    try:
                        st = workBook.add_sheet('站点' + str(self.target_station) + '采样数据')
                        st.write(0, 0, "NO.")
                        st.write(0, 1, "PGV_X(mm)")
                        st.write(0, 2, "PGV_Y(mm)")
                        st.write(0, 3, "PGV_R(°)")
                        st.write(0, 4, "AGV_X(mm)")
                        st.write(0, 5, "AGV_Y(mm)")
                        st.write(0, 6, "AGV_R(°)")
                    except Exception:
                        pass
                    workBook.save(XlsName)
                    a = self.ushort_to_short(NavStatus[3])
                    b = self.ushort_to_short(NavStatus[5])
                    c = self.ushort_to_short(NavStatus[7])
                    AGV_Xpos0 = round(a[0] / 1000, 4) * 1000
                    AGV_Ypos0 = round(b[0] / 1000, 4) * 1000
                    AGV_Rpos0 = round(c[0] / 1000 * 180 / 3.1415926, 2)
                    time.sleep(2)
                    break
                else:
                    time.sleep(1)
        # PGV连接
        bufsiz = 1024
        request_cmd_left = b'\xe8\x17'  # 请求命令，配置模式
        request_cmd = b'\xc8\x37'  # 请求命令，读位置信息
        socket.setdefaulttimeout(60)
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启套接字
        tcpCliSock.connect((self.PGV_IP, 4096))
        self.logger.info('PGV连接成功')
        tcpCliSock.send(request_cmd_left)  # 配置PGV
        response = tcpCliSock.recv(bufsiz)
        self.logger.info(response)
        # 开始直线前进到目标站点
        self.connection_status(self.AGV_IP)
        self.logger.info('前往目标站点', self.target_station)
        try:
            NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.target_station])
        except Exception as e:
            self.logger.error(" " + str(e))
            self.connection_status(self.AGV_IP)
        for i in range(5):
            self.connection_status(self.AGV_IP)  # 检查链接状态
            try:
                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
            except Exception as e:
                self.logger.error(" " + str(e))
                self.connection_status(self.AGV_IP)  # 断网重连
                self.connect_agv()
                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
            if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.target_station:
                time.sleep(5)
                try:
                    tcpCliSock.send(request_cmd)  # 发送读取位置信息
                    response = tcpCliSock.recv(bufsiz)  # 接受return信息
                    if not response:
                        self.logger.error('PGV Error')
                        break
                    if len(response) == 21:
                        new = struct.unpack('<bbbbbbbbbbbbbbbbbbbbb', bytes(response))  # 转换为字节
                        if new[0] & 0x03 == 0:
                            # 字节2~5转换为X方向坐标
                            xPos = (new[2] & 0x07) * 0x80 * 0x4000 + new[3] * 0x4000 + new[4] * 0x80 + new[5]
                            if xPos > 0x7fffff:
                                xPos = (xPos - 0xffffff) / 10
                            else:
                                xPos = xPos / 10
                            # 字节6~7转换为Y方向坐标
                            yPos = new[6] * 0x80 + new[7]
                            if yPos > 0x2000:
                                yPos = (yPos - 0x4000) / 10
                            else:
                                yPos = yPos / 10
                            # 字节10~11转换为角度值
                            Rod = new[10] * 0x80 + new[11]
                            Rod = Rod / 10
                except Exception as e:
                    self.logger.error('PGV Error' + str(e))
            else:
                time.sleep(1)


if __name__ == '__main__':
    unittest.main()
