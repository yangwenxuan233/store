# -*- coding: utf-8 -*-
# author ywx


import datetime
import math
import os
import socket
import struct
import time

import matplotlib.pyplot as plt
import modbus_tk.defines as cst
import xlrd
import xlutils.copy
import xlwings
import xlwt
from modbus_tk import modbus_tcp

import Standard_Modbus_Api


class Options():
    """静态方法类,包含了站点精度检测过程中的部分方法封装。
    无初始化参数
    Usage:
        import datetime
        import os
        import struct
        import time
        import xlrd
        import xlwt
        import xlutils.copy
        import matplotlib as plt
    """

    def Writexls(Name, add00, Par_rows, Par_X, Par_Y, Par_R, Par_AGV_X, Par_AGV_Y, Par_AGV_R, a='', b='', c='', Station_No=0) -> None:
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
        table.write(Par_rows, 7, a)
        table.write(Par_rows, 8, b)
        table.write(Par_rows, 9, c)
        excel.save(Name)

    def ushort_to_short(u_date: int) -> tuple:
        """AGV当前位置,无符号转换为有符号数。
        """
        Value0 = struct.pack("H", u_date)
        return struct.unpack("h", Value0)

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

    def data_analysis(xlsname: str) -> None:
        '''对已采集结束的数据进行处理。
        并对每个站点数据调用draw_graph方法生成散点图。
        param: xlsname: .xls文件名
        return: None
        '''
        excel = xlrd.open_workbook(xlsname)  # 用xlrd提供的方法读取一个excel文件
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
            Options.Writexls(xlsname, '最大值', rows+1, max(PGV_Xpos0), max(PGV_Ypos0), max(PGV_Rpos0),
                             max(AGV_Xpos0), max(AGV_Ypos0), max(AGV_Rpos0), Station_No=station)  # 统计最大值
            Options.Writexls(xlsname, '最小值', rows+2, min(PGV_Xpos0), min(PGV_Ypos0), min(PGV_Rpos0),
                             min(AGV_Xpos0), min(AGV_Ypos0), min(AGV_Rpos0), Station_No=station)  # 统计最小值
            Options.Writexls(xlsname, '极差', rows+3, Options.calculate_range(PGV_Xpos0), Options.calculate_range(PGV_Ypos0),
                             Options.calculate_range(PGV_Rpos0), Options.calculate_range(AGV_Xpos0),
                             Options.calculate_range(AGV_Ypos0), Options.calculate_range(AGV_Rpos0), Station_No=station)  # 统计极差
            # 生成折线图.png文件
            Options.draw_graph(PGV_Xpos0, 'PGV_Xpos0(mm)', station)
            Options.draw_graph(PGV_Ypos0, 'PGV_ypos0(mm)', station)
            Options.draw_graph(PGV_Rpos0, 'PGV_Rpos0(mm)', station)
            print('生成统计图完成')
            time.sleep(1)
            data_dict[station] = ['PGV_Xpos0(mm)', 'PGV_Ypos0(mm)', 'PGV_Rpos0(mm)']
        # 图片插入.xls文件
        try:
            Options.insert_png(xlsname, data_dict)
            print('数据处理完成')
        except Exception as e:
            print('图表插入失败: ' + str(e))

    def calculate_range(x: list):
        '''获取列表数据的极差
        '''
        return max([i for i in x]) - min([i for i in x])

    def draw_graph(data: list, title: str, station: int) -> None:
        '''根据传入的参数列表生成对应散点图。
        param: data: 数据, title: 散点图标题, station: 站点编号
        return: None
        '''
        plt.plot([i for i in range(1, len(data)+1)], data, alpha=0.8, marker='.')
        plt.title(title)
        plt.savefig(r'png\station' + str(station) + '_' + title + '.png')
        plt.close()

    def insert_png(xlsname: str, data_dict: dict) -> None:
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
            st.pictures.add(r'png\station' + str(i) + '_' + data_dict[i][0] + '.png',
                            left=st.range('K1').left, top=st.range('K1').top)
            st.pictures.add(r'png\station' + str(i) + '_' + data_dict[i][1] + '.png',
                            left=st.range('K28').left, top=st.range('K28').top)
            st.pictures.add(r'png\station' + str(i) + '_' + data_dict[i][2] + '.png',
                            left=st.range('K56').left, top=st.range('K56').top)
        wb.save(xlsname)  # 保存更改
        wb.close()  # 关闭文件资源
        app.quit()  # 退出


class PricitionDetection():
    """精度检测主要逻辑方法类。
    Usage:
        import datetime
        import socket
        import time
        import json
        import modbus_tk.defines as cst
        from modbus_tk import modbus_tcp
        import Standard_Matrix_HTTP_API

    """

    def __init__(self, AGV_IP: str, PGV_IP: str, speed_level: int) -> None:
        '''初始化IP地址,建立连接,配置参数1和参数2参数。
        :param:
            AGV_IP: AGV ip地址,
            PGV_IP: PGV ip地址,
            speed_level: 速度级别
        '''
        self.AGV_IP = AGV_IP
        self.PGV_IP = PGV_IP
        self.speed_level = speed_level
        self.connect_agv()
        self.param_setting()

    def param_setting(self) -> None:
        '''配置速度级别。
        '''
        modbus = Standard_Modbus_Api.SRPymodbus(self.AGV_IP)
        modbus.set_speed_level(self.speed_level)
        time.sleep(2)

    def connect_agv(self):
        '''modbus_tcp连接。
        '''
        self.MASTER = modbus_tcp.TcpMaster(host=self.AGV_IP, port=502)
        self.MASTER.set_timeout(30)
        print("connected")

    def main(self, stations: list, times: int) -> None:
        """精度检测逻辑主函数,支持同一路由的多站点精度检测。
        param: [站点1, 站点2, 站点3, ...], 采集次数
        type: list[int, int, int, ...], int
        return: None
        """

        if not stations:
            print("站点列表为空。")
            return
        elif len(stations) == 1:
            print("请至少填写两个站点。")
            return
        present_stations = stations  # 初始化目标站点列表
        present_data = {}  # 初始化当前数据行数记录
        for i in stations:
            present_data[i] = 1
        """缓存数据结构
        {
            station1: row_number,
            station2: row_number,
            station3: row_number,
            ... ,
        }
        """
        self.station = present_stations[0]  # 获取当前站点

        # 读取系统状态码
        Options.connection_status(self.AGV_IP)  # 检查链接状态
        try:
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
        except Exception as e:
            print(" " + str(e))
            Options.connection_status(self.AGV_IP)  # 断网重连
            self.connect_agv()
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取

        if NavStatus[0] == 2 and NavStatus[1] == 3:
            print('AGV状态正常')
            # 导航至起始站点
            Options.connection_status(self.AGV_IP)
            print('前往目标站点 ', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                print(" " + str(e))

            while True:
                time.sleep(3)
                Options.connection_status(self.AGV_IP)  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    # AGV状态正常，新建文件
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S.%f')
                    # 文件命名
                    XlsName = str(self.AGV_IP) + "_" + str(now_time) + "_" + str(self.speed_level) + '%' + ".xls"
                    workBook = xlwt.Workbook()  # built xls
                    # 创建对应站点数据sheet
                    for i in stations:
                        try:
                            st = workBook.add_sheet('站点' + str(i) + '采样数据')
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
                    a = Options.ushort_to_short(NavStatus[3])
                    b = Options.ushort_to_short(NavStatus[5])
                    c = Options.ushort_to_short(NavStatus[7])
                    AGV_Xpos0 = round(a[0] / 1000, 4) * 1000
                    AGV_Ypos0 = round(b[0] / 1000, 4) * 1000
                    AGV_Rpos0 = round(c[0] / 1000 * 180 / 3.1415926, 2)
                    # if AGV_Rpos0 < 0 :
                    # AGV_Rpos0 = AGV_Rpos0 + 360
                    time.sleep(2)
                    break
                else:
                    time.sleep(1)

        # host = "localhost"
        bufsiz = 1024
        # request_cmd_left = b'\xe8\x17'  # 请求命令，配置模式
        request_cmd = b'\xc8\x37'  # 请求命令，读位置信息
        socket.setdefaulttimeout(60)
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启套接字
        tcpCliSock.connect((self.PGV_IP, 4096))
        # tcpCliSock.settimeout(60)
        print('PGV连接成功')
        # tcpCliSock.send(request_cmd_left)  # 配置PGV
        # response = tcpCliSock.recv(bufsiz)
        # print(response)
        time.sleep(1)

        for add00 in range(1, times + 1):
            try:
                tcpCliSock.send(request_cmd)  # 发送读取位置信息
                response = tcpCliSock.recv(bufsiz)  # 接受return信息
                if not response:
                    break
                if len(response) == 21:
                    new = struct.unpack('<bbbbbbbbbbbbbbbbbbbbb', bytes(response))  # 转换为字节
                    if new[0] & 0x03 == 0:
                        # 字节2~5转换为X方向坐标
                        xPos = (new[2] & 0x07) * 0x80 * 0x4000 + new[3] * 0x4000 + new[4] * 0x80 + new[5]
                        if xPos > 0x2000:
                            xPos = (xPos - 0x4000) / 10
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
                        while True:
                            time.sleep(1)
                            Options.connection_status(self.AGV_IP)  # 检查链接状态
                            try:
                                NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                            except Exception as e:
                                print(" " + str(e))
                            if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                                a = Options.ushort_to_short(NavStatus[3])
                                b = Options.ushort_to_short(NavStatus[5])
                                c = Options.ushort_to_short(NavStatus[7])
                                a = round(a[0] / 1000, 4) * 1000
                                b = round(b[0] / 1000, 4) * 1000
                                c = round(c[0] / 1000 * 180 / 3.1415926, 2)
                                break
                        print(add00, "  ", self.station, "  ", xPos, yPos, Rod, AGV_Xpos0, AGV_Ypos0, AGV_Rpos0, a, b, c)

                        # 保存站点数据
                        if len(present_stations) == 1:
                            present_stations = stations  # 已到达末尾站点，重置目标站点列表
                        else:
                            present_stations = present_stations[1:]  # 刷新目标站点列表
                        Options.Writexls(XlsName, add00, present_data[self.station], xPos, yPos, Rod,
                                         AGV_Xpos0, AGV_Ypos0, AGV_Rpos0, a, b, c, self.station)  # 写入数据
                        present_data[self.station] += 1  # 对应站点行数计数
                        self.station = present_stations[0]  # 切换目标站点
                    else:
                        print("PGV Error")
                        if len(present_stations) == 1:
                            present_stations = stations  # 已到达末尾站点，重置目标站点列表
                        else:
                            present_stations = present_stations[1:]  # 刷新目标站点列表
                            Options.Writexls(XlsName, add00, present_data[self.station],
                                             0, 0, 0, 0, 0, 0, 0, 0, 0, self.station)
                            present_data[self.station] += 1  # 对应站点行数计数
                            self.station = present_stations[0]  # 切换目标站点
            except Exception:
                print("PGV Error")
                if len(present_stations) == 1:
                    present_stations = stations  # 已到达末尾站点，重置目标站点列表
                else:
                    present_stations = present_stations[1:]  # 刷新目标站点列表
                Options.Writexls(XlsName, add00, present_data[self.station],
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, self.station)
                present_data[self.station] += 1  # 对应站点行数计数
                self.station = present_stations[0]  # 切换目标站点

            # 采集结束前往新目标站点
            Options.connection_status(self.AGV_IP)
            print('前往目标站点', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                print(" " + str(e))
                Options.connection_status(self.AGV_IP)
            # 到达新站点采集数据
            while True:
                time.sleep(3)
                Options.connection_status(self.AGV_IP)  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                    Options.connection_status(self.AGV_IP)  # 断网重连
                    self.connect_agv()
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取

                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    time.sleep(5)
                    a = Options.ushort_to_short(NavStatus[3])
                    b = Options.ushort_to_short(NavStatus[5])
                    c = Options.ushort_to_short(NavStatus[7])
                    AGV_Xpos0 = round(a[0] / 1000, 4) * 1000
                    AGV_Ypos0 = round(b[0] / 1000, 4) * 1000
                    AGV_Rpos0 = round(c[0] / 1000 * 180 / math.pi, 2)
                    # if AGV_Rpos0 < 0 :
                    # AGV_Rpos0 = AGV_Rpos0 + 360
                    break
                else:
                    time.sleep(0.5)
            time.sleep(1)
        tcpCliSock.close()
        print('数据采集完成')
        # try:
        Options.data_analysis(XlsName)
        # except Exception as e:
        #     print('数据处理异常 ' + str(e))


if __name__ == '__main__':
    # 读取config文件中的参数
    try:
        with open("config.txt", "r", encoding='utf-8') as f:
            data = f.readlines()
        AGV_IP = data[1].replace('\n', '')
        PGV_IP = data[3].replace('\n', '')
        stations = [int(i) for i in data[5].strip().split(' ')]  # 站点列表
        times = int(data[7])
        speed_level = [int(i) for i in data[9].strip().split(' ')]
    except Exception:
        print('读取文件失败')
    print(AGV_IP, PGV_IP, stations, times, speed_level)
    for i in speed_level:
        print("当前速度级别: ", i)
        pd = PricitionDetection(AGV_IP, PGV_IP, i)
        pd.main(stations, times)
