import datetime
import os
import threading
import time
import xlrd
import xlutils.copy

import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import xlwt
from Standard_Modbus_Api import SRPymodbus


class TestConsumption():
    '''功耗检测脚本, 采集间隔1min。
    '''
    def __init__(self, AGV_IP) -> None:
        '''初始化IP地址,建立连接。
        '''
        self.AGV_IP = AGV_IP
        self.connect_agv()

    def connect_agv(self):
        '''modbus_tcp连接。
        '''
        self.MASTER = modbus_tcp.TcpMaster(host=self.AGV_IP, port=502)
        self.MASTER.set_timeout(30)

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
                with open("log.txt", "a+") as f:
                    f.write(str(datetime.datetime.now()) + "--" + str(self.AGV_IP) + "\n"
                            + detil[2] + "\n" + detil[-2] + "\n")
                    f.close()
                time.sleep(1)
            else:
                return

    def get_consumption(self):
        self.min += 1
        modbus = SRPymodbus(self.AGV_IP)
        data = modbus.read_input_register_battery_status()
        consumption = round(float(data['battery_voltage(V)']) * float(data['battery_current(A)']), 2)
        rexcel = xlrd.open_workbook(self.xlsname)  # 用xlrd提供的方法读取一个excel文件
        excel = xlutils.copy.copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet('功耗采样数据')  # 用xlwt对象的方法获得要操作的sheet
        # 写入对应数据
        now_time = datetime.datetime.now().strftime('%H-%M-%S.%f')
        table.write(self.min, 0, now_time)
        table.write(self.min, 1, consumption)
        excel.save(self.xlsname)

    def func_timer(self):
        self.get_consumption()
        global timer
        timer = threading.Timer(60, self.func_timer)
        self.min = 0
        timer.start()

    def main(self):
        try:
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
        except Exception as e:
            print(" " + str(e))
            self.connection_status()  # 断网重连
            self.connect_agv()
            NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取

        if NavStatus[0] == 2 and NavStatus[1] == 3:
            print('AGV状态正常')
            # AGV状态正常，新建文件
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S.%f')
            # 文件命名
            self.xlsname = str(self.AGV_IP) + "_" + str(now_time) + ".xls"
            workBook = xlwt.Workbook()  # built xls
            st = workBook.add_sheet('功耗采样数据')
            st.write(0, 0, "min")
            st.write(0, 1, "功率(W)")
            workBook.save(self.xlsname)
            self.min = 0
            self.func_timer()  # 启动计时器

        for i in range(30):
            self.station = 1
            print('前往目标站点', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                self.connect_agv()
                self.connection_status()  # 断网重连
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
                print(" " + str(e))
            while True:
                self.connection_status()  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                    self.connect_agv()
                    self.connection_status()  # 断网重连
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    break

            self.station = 2
            print('前往目标站点', self.station)
            try:
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            except Exception as e:
                self.connect_agv()
                self.connection_status()  # 断网重连
                NavStatus = self.MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
                print(" " + str(e))

            while True:
                self.connection_status()  # 检查链接状态
                try:
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")
                except Exception as e:
                    print(" " + str(e))
                    self.connect_agv()
                    self.connection_status()  # 断网重连
                    NavStatus = self.MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 16, data_format="")  # 重新读取
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    break
        timer.cancel()


if __name__ == '__main__':
    agv = TestConsumption('192.168.33.21')
    agv.main()
