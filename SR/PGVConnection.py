import socket
import time
import struct


class PGVApi():
    '''PGV对外接口api类,包含连接初始化,数据采集。
    :使用方法:
        import socket
        import time
        import struct
        PGV = PGVApi(ip, port)
        data = PGV.get_data()
    '''

    def __init__(self, ip, port) -> None:
        '''初始化PGV地址、端口,初次连接。
        :param:
            ip: PGV ip地址,
            port: PGV端口
        :retrun: None
        '''
        self.ip = ip
        self.port = port
        self.connection()

    def connection(self):
        '''建立socket连接并配置PGV。
        '''
        self.bufsiz = 1024
        self.request_cmd = b'\xc8\x37'  # 请求命令，读位置信息
        socket.setdefaulttimeout(3)  # 设置等待时间
        self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启套接字
        self.tcpCliSock.connect((self.ip, self.port))  # 建立连接
        print('PGV连接成功')
        time.sleep(1)

    def get_data(self):
        '''读取PGV数据。
        :param:
        :return: list[X方向坐标, Y方向坐标, 角度值]
        '''
        try:
            self.tcpCliSock.send(self.request_cmd)  # 发送读取位置信息
            response = self.tcpCliSock.recv(self.bufsiz)  # 接受return信息
            if not response:
                return "PGV Error"
            elif len(response) == 21:
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
                    return [xPos, yPos, Rod]
            else:
                return "PGV Error"
        except Exception:
            return "PGV Error"


if __name__ == '__main__':
    pgv = PGVApi('10.10.100.254', 4096)
    while True:
        data = pgv.get_data()
        print(data)
