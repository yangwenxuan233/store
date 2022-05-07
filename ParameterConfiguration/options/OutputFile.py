from config.ParameterSettings import ParameterSettings
from libs.TextFile import TextFile
from PyQt5.QtWidgets import QFileDialog


class OutputFile():
    # 导出文件
    def output_file(list1):
        path = QFileDialog.getExistingDirectory(None, "选取文件夹", "D:/")  # 起始路径
        list2 = []
        for i in ParameterSettings.base_parameter:
            if i.startswith('null'):
                pass
            else:
                list2.append(i)
        if list1 != []:
            try:
                TextFile.write_txt(path, list1, list2)
                return "<font color='green' size='5'><green>导出文件完成。</font>"
            except Exception as e:
                return "<font color='red' size='5'><red>导出文件失败!" + str(e) + "</font>"
