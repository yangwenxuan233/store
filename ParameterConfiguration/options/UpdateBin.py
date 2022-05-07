import socket
import time

from config.ParameterSettings import ParameterSettings


class UpdateBin():
    # 程序更新
    def update_bin(bin_file, Size, size, c):
        # 组建新格式数据包

        I_range = int(Size / 1024)
        for i in range(I_range):
            number = bin_file.read(1024)  # 每次输出1024个字节
            n = b'\x54\x3F\x51\xA5'  # 包头识别位
            m = b'\x55\xa1\x0f\x41'  # 包尾识别位
            # 第一个数据包
            if i == 0:
                t = b'\x11'  # 第一包识别位
                number = n + t + number + m
            # 中间数据包
            elif 0 < i < (Size / 1024 - 1):
                d = b'\x01'  # 中间包识别位
                number = n + d + number + m
            # 最后一个数据包
            elif i == (Size / 1024 - 1):
                # input('e')
                f = b'\x31'  # 最后一包识别位
                if size % 1024 != 0:
                    for jj in range(c):
                        o = b'\x00'  # 补零
                        number = number + o
                    number = n + f + number + m
                else:
                    number = n + f + number + m
            else:
                break
            # 建立发送连接
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.bind(("192.168.1.77", 2368))  # 本机IP，端口号
                s.sendto(number, ParameterSettings.addr)  # 发送UDP数据包到客户端
                s.shutdown(2)  # 关闭发送和接收通道
                s.close()  # 断开连接
            except Exception:
                # self.textEdit.setPlainText('上位机连接超时!')
                return "<font color='red' size='5'><red>请求地址无效，上位机连接超时!</font>" + '\n'

            # 建立接收连接
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("192.168.1.77", 8080))
            s.settimeout(5)
            try:
                data, add = s.recvfrom(2048)  # 获取UDP数据
                lenth = len(data)  # 接收包长度
                s.settimeout(5)  # 设置未获取数据延时5s
                start_time = time.time()  # 开始计时
                # 判断接收包长度
                while (lenth != 10):
                    data, add = s.recvfrom(2048)
                    lenth = len(data)
                    end_time = time.time()  # 结束计时
                    derta_time = end_time - start_time  # 循环时间
                    # 判断循环时间是否超时，上限60s
                    if derta_time < 60:
                        continue
                    else:
                        break
                s.shutdown(2)
                s.close()  # 断开连接
                if lenth == 10:
                    continue
                else:
                    # print('上位机未接收到合适的数据包超时60s，关闭通道')
                    # self.textEdit.setPlainText('上位机未接收到合适的数据包超时60s，关闭通道')
                    return "<font color='red' size='5'><red>上位机未接收到合适的数据包超时60s，关闭通道!</font>" + '\n'
            except Exception:
                s.shutdown(2)
                s.close()  # 断开连接
                # print('上位机接收数据超时5s，关闭通道')
                # self.textEdit.setPlainText('上位机接收数据超时5s，关闭通道')
                return "<font color='red' size='5'><red>上位机接收数据超时5s，关闭通道!</font>" + '\n'
        if i == 0:
            bin_file.close()  # 关闭bin文件
        else:
            bin_file.close()  # 关闭bin文件
            return "<font color='blue' size='5'><blue>下载完成。</font>" + '\n'
