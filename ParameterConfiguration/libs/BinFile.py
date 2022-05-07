import os

from config.ParameterSettings import ParameterSettings
from PyQt5.QtWidgets import QFileDialog


class BinFile():

    def read_bin():
        # 读取bin文件
        m = QFileDialog.getOpenFileName(None, "打开文件", "D:/", "Text Files (*.bin)")  # 起始路径
        print("Receive from %s:%s" % ParameterSettings.addr)
        filepath = str(m[0])  # 文件路径
        bin_file = open(filepath, 'rb')  # 读取.bin文件
        size = os.path.getsize(filepath)  # 获得文件大小

        # 判断、分割数据包
        if size % 1024 == 0:
            Size = size
        elif size % 1024 != 0:
            c = 1024 - size % 1024  # 需求补零数
            Size = size + c

        print(bin_file, Size, size, c)
        return bin_file, Size, size, c




