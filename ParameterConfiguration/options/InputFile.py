from PyQt5.QtWidgets import QFileDialog

from libs.TextFile import TextFile


class InputFile():
    # 导入文件
    def input_file(list):
        try:
            m = QFileDialog.getOpenFileName(None, "打开文件", "D:/", "Text Files (*.txt)")  # 起始路径
            path = m[0]
            list = TextFile.read_txt(path)
            return list
        except Exception as e:
            return "<font color='red' size='5'><red>文件导入失败失败!" + str(e) + "</font>"
