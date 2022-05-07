import datetime
import json
import os
import socket
import struct
import time
import unittest

import ddt
import matplotlib.pyplot as plt
import modbus_tk.defines as cst
import paramiko
import xlrd
import xlutils.copy
import xlwings
import xlwt
from modbus_tk import modbus_tcp
from ST_test_frame.common.logs import Logs
from ST_test_frame.common.martix_api import Standard_Matrix_Api
from ST_test_frame.common.modbus_api import Standard_Modbus_Api
from ST_test_frame.config import settings


@ddt.ddt
class TestStation(unittest.TestCase):
    '''Oasis站点精度用例, 直线站点精度-空载前进。
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
        self.logger.info("AGV connected")

    def connect_pgv(self):
        '''socket连接。
        '''
        self.bufsiz = 1024
        # self.request_cmd_left = b'\xe8\x17'  # 请求命令，配置模式
        self.request_cmd = b'\xc8\x37'  # 请求命令，读位置信息
        socket.setdefaulttimeout(30)
        self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启套接字
        self.tcpCliSock.connect((self.PGV_IP, self.PGV_port))
        self.logger.info('PGV连接成功')
        # self.tcpCliSock.send(self.request_cmd_left)  # 配置PGV
        # response = self.tcpCliSock.recv(self.bufsiz)
        # self.assertIsNotNone(response)

    def param_setting(self) -> None:
        '''配置速度级别和减速度, 自动重启系统。
        '''
        matrix = Standard_Matrix_Api.SR_Matrix_HTTP(self.AGV_IP)
        # 关闭自由导航
        matrix.modify_single_parameter(417, {'value': 'False'})
        # 配置速度
        matrix.modify_single_parameter(5301, {'value': self.speed})
        # 配置减速度
        matrix.modify_single_parameter(5304, {'value': self.acc_down})
        # 开启modbus_tcp
        matrix.modify_single_parameter(2101, {'value': 'True'})
        time.sleep(2)
        # 重启SROS
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts中的主机
        ssh.connect(hostname=self.AGV_IP, port=2222, username='root', password='SRpasswd@2017')  # 建立连接
        stdin, stdout, stderr = ssh.exec_command('systemctl restart sros')  # 重启sros服务
        self.logger.info('正在重启SROS')
        time.sleep(20)
        ssh.close()
        # 解除重启后软急停状态
        modbus = Standard_Modbus_Api.SRPymodbus(self.AGV_IP)
        modbus.write_single_coil_function('解除急停')
        time.sleep(2)
        result = modbus.read_discrete_inputs(10001)
        self.assertEqual(False, result)
        self.logger.info('解除急停成功')
        # 检查参数状态
        speed = int(dict(json.loads(matrix.get_single_config_parameter(5301)))['value'])
        acc_down = int(dict(json.loads(matrix.get_single_config_parameter(5304)))['value'])
        self.assertEqual(speed, self.speed)
        self.assertEqual(acc_down, self.acc_down)
        self.logger.info('参数设置成功, 当前最大线速度: ' + str(self.speed) + ' 当前减速度: ', str(self.acc_down))

    def connection_status(self) -> None:
        """检测当前ip地址连接状态。
        畅通时直接返回, 反之则记录当前时间和日志信息。
        """
        while True:
            backinfo = os.popen(f"ping -w 1 {self.AGV_IP}").read()
            detil = str(backinfo).split('\n')
            if str(backinfo).find("回复") == -1:
                # 记录时间和返回值
                self.logger.info(str(datetime.datetime.now()) + "--" + str(self.AGV_IP)
                                 + "\n" + detil[2] + "\n" + detil[-2] + "\n")
                self.connect_agv()
                time.sleep(1)
            else:
                return

    def ushort_to_short(self, u_date: int) -> tuple:
        """AGV当前位置,无符号转换为有符号数。
        """
        Value0 = struct.pack("H", u_date)
        return struct.unpack("h", Value0)

    def get_agv_data(self, NavStatus):
        '''获取AGV当前位置参数。
        '''
        a = self.ushort_to_short(NavStatus[3])
        b = self.ushort_to_short(NavStatus[5])
        c = self.ushort_to_short(NavStatus[7])
        AGV_Xpos = round(a[0] / 1000, 4) * 1000
        AGV_Ypos = round(b[0] / 1000, 4) * 1000
        AGV_Rpos = round(c[0] / 1000 * 180 / 3.1415926, 2)
        return [AGV_Xpos, AGV_Ypos, AGV_Rpos]

    def get_pgv_data(self):
        '''获取PGV当前位置数据。
        '''
        try:
            self.tcpCliSock.send(self.request_cmd)  # 发送读取位置信息
            response = self.tcpCliSock.recv(self.bufsiz)  # 接受return信息
        except Exception:
            self.connect_pgv()
            self.tcpCliSock.send(self.request_cmd)  # 发送读取位置信息
            response = self.tcpCliSock.recv(self.bufsiz)  # 接受return信息
        if len(response) == 21:
            new = struct.unpack('<bbbbbbbbbbbbbbbbbbbbb', bytes(response))
            if new[0] & 0x03 == 0:
                Xpos = (new[2] & 0x07) * 0x80 * 0x4000 + new[3] * 0x4000 + new[4] * 0x80 + new[5]
                if Xpos > 0x7fffff:
                    Xpos = (Xpos - 0xffffff) / 10
                else:
                    Xpos = Xpos / 10
                # 字节6~7转换为Y方向坐标
                Ypos = new[6] * 0x80 + new[7]
                if Ypos > 0x2000:
                    Ypos = (Ypos - 0x4000) / 10
                else:
                    Ypos = Ypos / 10
                # 字节10~11转换为角度值
                Rod = new[10] * 0x80 + new[11]
                Rod = Rod / 10
        else:
            self.logger.info('PGV Error')
            Xpos = Ypos = Rod = 0
        return [Xpos, Ypos, Rod]

    def write_xls(self, Name, add00, Par_rows, Par_X, Par_Y, Par_R, Par_AGV_X, Par_AGV_Y, Par_AGV_R, Station_No=0) -> None:
        """对已创建的.xls文件进行数据写入操作。
        param: 文件名, 数据编号, 行位置, PGV X方向, PGV X方向, PGV角度, AGV X方向, AGV Y方向, AGV角度, 站点编号
        type: str, int, int, float, float, float, float, float, float, int
        return: None
        """

        rexcel = xlrd.open_workbook(Name)  # 用xlrd提供的方法读取一个excel文件
        excel = xlutils.copy.copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet('站点' + str(Station_No) + '采样数据')  # 用xlwt对象的方法获得要操作的sheet
        # 写入对应数据
        table.write(Par_rows, 0, add00)  # 数据编号
        table.write(Par_rows, 1, Par_X)  # PGV X方向
        table.write(Par_rows, 2, Par_Y)  # PGV Y方向
        table.write(Par_rows, 3, Par_R)  # PGV角度
        table.write(Par_rows, 4, Par_AGV_X)  # AGV X方向
        table.write(Par_rows, 5, Par_AGV_Y)  # AGV Y方向
        table.write(Par_rows, 6, Par_AGV_R)  # AGV角度
        excel.save(Name)

    def data_analysis(self) -> None:
        '''对已采集结束的数据进行处理。
        并对每个站点数据调用draw_graph方法生成散点图。
        '''
        excel = xlrd.open_workbook(self.xlsname)  # 用xlrd提供的方法读取一个excel文件
        sheets = excel.sheet_names()  # 获取所有sheet名
        data_dict = {}  # 初始化数据缓存字典
        for i in sheets:
            station = int("".join(list(filter(str.isdigit, i))))  # 获取当前sheet站点编号
            st = excel.sheet_by_name(i)  # 获取sheet对象
            rows = st.nrows  # 获取行数
            # 初始化数据缓存列表
            PGV_Xpos0 = []
            PGV_Ypos0 = []
            PGV_Rpos0 = []
            AGV_Xpos0 = []
            AGV_Ypos0 = []
            AGV_Rpos0 = []
            # 缓存sheet中6个参数数据
            for j in range(1, rows):
                data = st.row_values(j)
                PGV_Xpos0.append(data[1])
                PGV_Ypos0.append(data[2])
                PGV_Rpos0.append(data[3])
                AGV_Xpos0.append(data[4])
                AGV_Ypos0.append(data[5])
                AGV_Rpos0.append(data[6])
            # 写入极差数据
            self.write_xls(self.xlsname, '最大值', rows+1, max(PGV_Xpos0), max(PGV_Ypos0), max(PGV_Rpos0),
                           max(AGV_Xpos0), max(AGV_Ypos0), max(AGV_Rpos0), station)  # 统计最大值
            self.write_xls(self.xlsname, '最小值', rows+2, min(PGV_Xpos0), min(PGV_Ypos0), min(PGV_Rpos0),
                           min(AGV_Xpos0), min(AGV_Ypos0), min(AGV_Rpos0), station)  # 统计最小值
            self.write_xls(self.xlsname, '极差', rows+3, self.calculate_range(PGV_Xpos0), self.calculate_range(PGV_Ypos0),
                           self.calculate_range(PGV_Rpos0), self.calculate_range(AGV_Xpos0),
                           self.calculate_range(AGV_Ypos0), self.calculate_range(AGV_Rpos0), station)  # 统计极差
            # 生成折线图.png文件
            self.draw_graph(PGV_Xpos0, 'PGV_Xpos0(mm)', station)
            self.draw_graph(PGV_Ypos0, 'PGV_ypos0(mm)', station)
            self.draw_graph(PGV_Rpos0, 'PGV_Rpos0(mm)', station)
            self.logger.info('生成统计图完成')
            data_dict[station] = ['PGV_Xpos0(mm)', 'PGV_Ypos0(mm)', 'PGV_Ypos0(mm)']
            time.sleep(2)
        # 图片插入.xls文件
        # try:
        self.insert_png(self.xlsname, data_dict)
        self.logger.info('数据处理完成')
        # except Exception:
        #     self.logger.error('图表插入失败')

    def calculate_range(self, x: list):
        '''获取列表数据的极差
        '''
        return max([i for i in x]) - min([i for i in x])

    def draw_graph(self, data: list, title: str, station: int) -> None:
        '''根据传入的参数列表生成对应散点图。
        param: data: 数据, title: 散点图标题, station: 站点编号
        return: None
        '''
        plt.plot([i for i in range(1, len(data)+1)], data, alpha=0.8, marker='.')
        plt.title(title)
        plt.savefig(os.path.join(self.out_path, r'station' + str(station) + '_' + title + '.png'))
        plt.close()

    def insert_png(self, xlsname: str, data_dict: dict) -> None:
        '''将图片插入表格特定位置。
        param: xlsname: xls文件名, data_dict: 缓存数据
        return: None
        '''
        app = xlwings.App(visible=False, add_book=False)  # 关闭前台显示，关闭添加工作簿
        wb = app.books.open(xlsname)  # 打开xls文件
        app.display_alerts = False  # 关闭一些提示信息。默认为True
        app.screen_updating = False  # 关闭更新显示工作内容。默认为True
        for i in data_dict:
            st = wb.sheets['站点' + str(i) + '采样数据']  # 选择sheet
            # 插入图片
            st.pictures.add(os.path.join(self.out_path, r'station' + str(i) + '_' + data_dict[i][0] + '.png'),
                            left=st.range('I1').left, top=st.range('I1').top)
            st.pictures.add(os.path.join(self.out_path, r'station' + str(i) + '_' + data_dict[i][1] + '.png'),
                            left=st.range('I28').left, top=st.range('I28').top)
            st.pictures.add(os.path.join(self.out_path, r'station' + str(i) + '_' + data_dict[i][2] + '.png'),
                            left=st.range('I56').left, top=st.range('I56').top)
        wb.save(xlsname)  # 保存更改
        wb.close()  # 关闭文件资源
        app.quit()  # 退出

    @ddt.file_data(settings.OASIS_YAML)
    def test_straight_forward_nonload(self, **kwargs):
        '''用例分类: 直线站点精度-空载前进, 用例标题: 空载、速度0.3m/s、减速度0.1m/s²、直线前进,
        预期结果: 站点精度 < ±10mmm 偏角 < ±0.5°
        '''
        self.AGV_IP = kwargs['agv_ip']
        self.PGV_IP = kwargs['pgv_ip']
        self.PGV_port = kwargs['pgv_port']
        self.speed = int(kwargs['speed'][0])
        self.acc_down = int(kwargs['acc_down'][0])
        self.load = kwargs['load'][0]
        self.stations = kwargs['stations'][0]
        self.times = kwargs['times']
        self.target_station = int(kwargs['target_station'][0])
        self.out_path = settings.OASIS_DATA
        self.connect_agv()
        self.param_setting()
        self.connect_pgv()
        present_stations = self.stations  # 初始化目标站点列表
        present_data = {}  # 初始化当前数据行数记录
        for i in self.stations:
            present_data[i] = 1
        """缓存数据结构
        {
            station1: row_number,
            station2: row_number,
            station3: row_number,
            ... ,
        }
        """
        # 创建过程数据存储文件
        now_time = datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S.%f')
        self.xlsname = os.path.join(self.out_path, str(self.AGV_IP) + "_" + str(now_time) + "_" + self.load + "_"
                                    + str(self.speed) + "_" + str(self.acc_down) + ".xls")
        wb = xlwt.Workbook()
        st = wb.add_sheet('站点' + str(self.target_station) + '采样数据')
        st.write(0, 0, "NO.")
        st.write(0, 1, "PGV_X(mm)")
        st.write(0, 2, "PGV_Y(mm)")
        st.write(0, 3, "PGV_R(°)")
        st.write(0, 4, "AGV_X(mm)")
        st.write(0, 5, "AGV_Y(mm)")
        st.write(0, 6, "AGV_R(°)")
        self.logger.info(1)
        wb.save(self.xlsname)

        self.logger.info('test start')
        for i in range(1, self.times * len(self.stations) + 1):
            self.station = present_stations[0]  # 获取当前站点
            self.connection_status()  # 检查链接状态
            try:
                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 获取状态
            except Exception as e:
                self.logger.info(" " + str(e))
                self.connection_status()  # 断网重连
                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
            # 检查AGV当前状态
            if NavStatus[0] == 2 and NavStatus[1] == 3:
                self.logger.info('AGV状态正常')
                self.connection_status()
                self.logger.info('前往站点', self.station)
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            # 等待到达目标站点
            while True:
                self.connection_status()
                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    break
            if len(present_stations) == 1:
                present_stations = self.stations
            else:
                present_stations = present_stations[1:]
            if self.station == 2:
                agv_data = self.get_agv_data(NavStatus)
                pgv_data = self.get_pgv_data()
                self.logger.info(present_data[self.station], agv_data, pgv_data)
                self.write_xls(self.xlsname, i, present_data[self.station], agv_data[0], agv_data[1], agv_data[2],
                               pgv_data[0], pgv_data[1], pgv_data[2], self.station)
                present_data[self.station] += 1
                self.station = present_stations[0]
        self.tcpCliSock.close()
        self.logger.info('数据采集完成')
        self.data_analysis()


if __name__ == '__main__':
    unittest.main()
