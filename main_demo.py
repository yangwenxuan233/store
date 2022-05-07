import datetime
import struct
import time
from socket import *

import modbus_tk
import modbus_tk.defines as cst
import xlrd
import xlutils.copy
import xlwt
from modbus_tk import modbus_tcp


class Options():
    """静态方法类,包含了站点精度检测过程中的部分方法封装。
    无初始化参数
    """

    def Writexls(Name, add00, Par_rows, Par_X, Par_Y, Par_R, Par_AGV_X, Par_AGV_Y, Par_AGV_R, Station_No=0):
        """对已创建的.xls文件进行数据写入操作。
        入参: 文件名, 数据编号, 行位置, PGV X方向, PGV X方向, PGV角度, AGV X方向, AGV Y方向, AGV角度, 测试站点编号
        返回: None
        """

        rexcel = xlrd.open_workbook(Name)  # 用xlrd提供的方法读取一个excel文件
        excel = xlutils.copy.copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        # 用xlwt对象的方法获得要操作的sheet
        if Station_No == 0:
            table = excel.get_sheet_by_name('数据极差统计')
        else:
            table = excel.get_sheet_by_name('站点' + str(Station_No) + '采样数据')
        # 写入对应数据
        table.write(Par_rows, 0, add00)  # 数据编号
        table.write(Par_rows, 1, Par_X)  # PGV X方向
        table.write(Par_rows, 2, Par_Y)  # PGV Y方向
        table.write(Par_rows, 3, Par_R)  # PGV角度
        table.write(Par_rows, 4, Par_AGV_X)  # AGV X方向
        table.write(Par_rows, 5, Par_AGV_Y)  # AGV Y方向
        table.write(Par_rows, 6, Par_AGV_R)  # AGV角度
        excel.save(Name)

    def ushort_to_short(u_date):
        """AGV当前位置,无符号转换为有符号数。
        """
        Value0 = struct.pack("H", u_date)
        return struct.unpack("h", Value0)


class PricitionDetection():
    """精度检测逻辑方法类。
    调用方法:
        pd = PriciptionDetection(AGV_IP, PGV_IP)
        pd.main([station1, station2, station3, ...])
    """

    # 初始化连接地址
    def __init__(self, AGV_IP, PGV_IP) -> None:
        self.AGV_IP = AGV_IP
        self.PGV_IP = PGV_IP

    def main(self, stations):
        """精度检测逻辑主函数,支持闭环路线的多站点精度检测。
        入参: [站点1, 站点2, 站点3, ... ]
        type: list[int, int, int, ...]
        返回: None
        """

        present_stations = stations  # 初始化目标站点列表
        present_rows = {}  # 初始化当前数据行数记录
        for i in stations:
            present_rows[i] = 1
        """
        {
            station1 : 1,
            station2 : 1,
            station3 : 1,
            ... ,
            '极差' : 1
        }
        """
        self.station = present_stations[0]  # 获取当前站点

        LOGGER = modbus_tk.utils.create_logger("console")  # modbus -TCP连接
        MASTER = modbus_tcp.TcpMaster(host=self.AGV_IP, port=502)
        MASTER.set_timeout(5.0)
        LOGGER.info("connected")
        NavStatus = MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 19, data_format="")
        if NavStatus[0] == 2 and NavStatus[1] == 3:
            print("""1222""")
            NavStatus = MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            time.sleep(2)
            while True:
                NavStatus = MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 19, data_format="")
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    # AGV状态正常，新建文件
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S.%f')
                    XlsName = "Demo " + str(self.AGV_IP) + "_" + str(now_time) + ".xls"
                    workBook = xlwt.Workbook()  # built xls
                    # 创建对应站点数据sheet
                    for i in stations:
                        st = workBook.add_sheet('站点' + str(i) + '采样数据')
                        st.write(0, 0, "NO.")
                        st.write(0, 1, "PGV_X(mm)")
                        st.write(0, 2, "PGV_Y(mm)")
                        st.write(0, 3, "PGV_R(°)")
                        st.write(0, 4, "AGV_X(mm)")
                        st.write(0, 5, "AGV_Y(mm)")
                        st.write(0, 6, "AGV_R(°)")
                    # 创建极差数据统计sheet
                    st = workBook.add_sheet('数据极差统计')
                    st.write(0, 0, "NO.")
                    st.write(0, 1, "PGV_X(mm)")
                    st.write(0, 2, "PGV_Y(mm)")
                    st.write(0, 3, "PGV_R(°)")
                    st.write(0, 4, "AGV_X(mm)")
                    st.write(0, 5, "AGV_Y(mm)")
                    st.write(0, 6, "AGV_R(°)")
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
        request_cmd_left = b'\xe8\x17'  # 请求命令，配置模式
        request_cmd = b'\xc8\x37'  # 请求命令，读位置信息
        tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 开启套接字
        tcpCliSock.connect((self.PGV_IP, 4096))
        tcpCliSock.send(request_cmd_left)  # 配置PGV
        print("""1223""")
        response = tcpCliSock.recv(bufsiz)
        print(response)
        time.sleep(1)

        for add00 in range(1, 10001):
            tcpCliSock.send(request_cmd)  # 发送读取位置信息
            response = tcpCliSock.recv(bufsiz)  # 接受返回信息
            # print(response)
            if not response:
                break
            if len(response) == 21:
                new = struct.unpack('<bbbbbbbbbbbbbbbbbbbbb', bytes(response))  # 转换为字节
                # print(new)
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
                    print(add00, "       ", self.station, "  ", xPos, yPos, Rod, AGV_Xpos0, AGV_Ypos0, AGV_Rpos0)
                    # 首次采集数据记录
                    if add00 == 1:
                        MAX_xPos = xPos
                        MAX_yPos = yPos
                        MAX_Rod = Rod
                        MAX_AGV_Xpos0 = AGV_Xpos0
                        MAX_AGV_Ypos0 = AGV_Ypos0
                        MAX_AGV_Rpos0 = AGV_Rpos0
                        Min_xPos = xPos
                        Min_yPos = yPos
                        Min_Rod = Rod
                        Min_AGV_Xpos0 = AGV_Xpos0
                        Min_AGV_Ypos0 = AGV_Ypos0
                        Min_AGV_Rpos0 = AGV_Rpos0
                    # 重复采集获取最大值和最小值
                    MAX_xPos = max(MAX_xPos, xPos)
                    MAX_yPos = max(MAX_yPos, yPos)
                    MAX_Rod = max(MAX_Rod, Rod)
                    MAX_AGV_Xpos0 = max(MAX_AGV_Xpos0, AGV_Xpos0)
                    MAX_AGV_Ypos0 = max(MAX_AGV_Ypos0, AGV_Ypos0)
                    MAX_AGV_Rpos0 = max(MAX_AGV_Rpos0, AGV_Rpos0)
                    Min_xPos = min(Min_xPos, xPos)
                    Min_yPos = min(Min_yPos, yPos)
                    Min_Rod = min(Min_Rod, Rod)
                    Min_AGV_Xpos0 = min(Min_AGV_Xpos0, AGV_Xpos0)
                    Min_AGV_Ypos0 = min(Min_AGV_Ypos0, AGV_Ypos0)
                    Min_AGV_Rpos0 = min(Min_AGV_Rpos0, AGV_Rpos0)

                    # 保存站点数据
                    if len(present_stations) == 1:
                        present_stations = stations  # 已到达末尾站点，重置目标站点列表
                    else:
                        present_stations = present_stations[1:]  # 刷新目标站点列表
                    Options.Writexls(XlsName, add00, present_rows[self.station], xPos, yPos, Rod,
                                     AGV_Xpos0, AGV_Ypos0, AGV_Rpos0, self.station)  # 写入数据
                    present_rows[self.station] += 1  # 对应站点行数计数
                    self.station = present_stations[0]  # 切换目标站点

                    # 保存极差数据,每300次数据采集保存一次
                    if add00 % 300 == 0:
                        Options.Writexls(XlsName, add00, present_rows['极差'], MAX_xPos, MAX_yPos, MAX_Rod,
                                         MAX_AGV_Xpos0, MAX_AGV_Ypos0, MAX_AGV_Rpos0)
                        present_rows['极差'] += 1
                        Options.Writexls(XlsName, add00, present_rows['极差'], Min_xPos, Min_yPos, Min_Rod,
                                         Min_AGV_Xpos0, Min_AGV_Ypos0, Min_AGV_Rpos0)
                        present_rows['极差'] += 1
                        Options.Writexls(XlsName, add00, present_rows['极差'], MAX_xPos - Min_xPos, MAX_yPos - Min_yPos,
                                         MAX_Rod - Min_Rod, MAX_AGV_Xpos0 - Min_AGV_Xpos0, MAX_AGV_Ypos0 - Min_AGV_Ypos0,
                                         MAX_AGV_Rpos0 - Min_AGV_Rpos0)
                        present_rows['极差'] += 2
                else:
                    print("PGV Error")

            NavStatus = MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 40015, 1, output_value=[self.station])
            time.sleep(2)
            while True:
                NavStatus = MASTER.execute(1, cst.READ_INPUT_REGISTERS, 30001, 19, data_format="")
                if NavStatus[0] == 2 and NavStatus[1] == 3 and NavStatus[15] == 1 and NavStatus[14] == self.station:
                    time.sleep(5)
                    a = Options.ushort_to_short(NavStatus[3])
                    b = Options.ushort_to_short(NavStatus[5])
                    c = Options.ushort_to_short(NavStatus[7])
                    AGV_Xpos0 = round(a[0] / 1000, 4) * 1000
                    AGV_Ypos0 = round(b[0] / 1000, 4) * 1000
                    AGV_Rpos0 = round(c[0] / 1000 * 180 / 3.1415926, 2)
                    # if AGV_Rpos0 < 0 :
                    # AGV_Rpos0 = AGV_Rpos0 + 360
                    break
                else:
                    time.sleep(0.5)
            time.sleep(1)
        tcpCliSock.close()


# if __name__ == '__main__':
#     pd = PricitionDetection("192.168.33.135", "192.168.33.12")
#     pd.main([])
