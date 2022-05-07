import socket

import psutil

from DataStruct import DataStruct


class DataMonitor():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("192.168.1.77", 2368))
    net = ""

    def set_net(self):
        net_infor = psutil.net_if_addrs()
        for i in net_infor:
            if '192.168.1.77' in net_infor[i][1]:
                self.net = i
                return

    def get_net(self):
        return self.net

    def get_freq(self):
        # 点频自适应
        self.s.settimeout(0.05)
        data, add = self.s.recvfrom(2048)  # 获取UDP数据
        a1 = int(DataStruct.struct_unpack_two(data[2: 4])) / 100
        a2 = int(DataStruct.struct_unpack_two(data[8: 10])) / 100
        angle_resolution = a2 - a1
        if 0.05 <= angle_resolution <= 0.07:
            return 24  # 点频60k，freq = 24
        elif 0.11 <= angle_resolution <= 0.13:
            return 12  # 点频30k，freq = 12
        else:
            return 6  # 点频15k，freq = 6

    def data_monitor(self, freq, count, part_loss, complete_loss, last_angle):
        # 数据吞吐量统计
        # start = psutil.net_io_counters([True])[self.net][1]
        # begin = datetime.datetime.now()
        angle_per_package = 276.48/freq
        for i in range(freq):
            # 获取UDP数据
            DATA, add = self.s.recvfrom(2048)
            # 判断是否部分丢包
            if len(DATA) < 1206:
                count += 1
                part_loss += 1
            else:
                count += 1
                if last_angle is None:
                    last_angle = int(DataStruct.struct_unpack_two(DATA[2: 4])) / 100
                else:
                    # 获取首个点角度值
                    angle = int(DataStruct.struct_unpack_two(DATA[2: 4])) / 100
                    # 判断是否完整丢包
                    # 连续角度
                    if angle_per_package - (angle_per_package/192)*2 < angle - last_angle < angle_per_package + (angle_per_package/192)*2:
                        last_angle = angle
                    # 跨盲区
                    elif angle_per_package - (angle_per_package/192)*2 < angle - 45 + 315 - last_angle < angle_per_package + (angle_per_package/192)*2:
                        last_angle = angle
                    else:
                        # 连续角度丢包
                        if angle > last_angle:
                            # 四舍五入取丢包数
                            complete_loss += int(round((angle - last_angle)/angle_per_package, 0))
                        # 跨盲区丢包
                        elif angle < last_angle:
                            complete_loss += int(round((angle - 45 + 315 - last_angle)/angle_per_package, 0))
                        last_angle = angle
        # stop = psutil.net_io_counters([True])[self.net][1]
        # end = datetime.datetime.now()
        # bytes = stop - start
        # time = end - begin
        if count > 0:
            return count, part_loss, complete_loss, last_angle
        else:
            return count, 0, 0, None

# a = DataMonitor()
# freq = a.get_freq()
# a.set_net('以太网 2')
# count, part_loss, complete_loss, last_angle = 0, 0, 0, None
# for i in range(10000):
#     count, part_loss, complete_loss, last_angle, data, time = a.data_monitor(freq, count, part_loss, complete_loss, last_angle)
#     print("总数据包:", count, "部分丢包数:", part_loss, "完全丢包数:", complete_loss, "丢包率:", round(((part_loss + complete_loss)/count)*100, 4), "%", "传输速率:", round((data*8/time)/1024/1024, 4), "Mb/s")
