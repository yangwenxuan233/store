import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import mainWindow

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 开启防火墙权限
if __name__ == '__main__':
    try:
        # 获取解释器路径
        python_path = sys.executable
        # 获取解释器权限
        data = os.popen('netsh advfirewall firewall show rule name=python').readlines()
        if all(['规则名称:                             python\n' not in data, '操作:                                 允许\n' not in data]):
            os.system('netsh advfirewall firewall add rule name="python" dir=in action=allow program=' + python_path + ' enable=yes')
        print('权限开启成功')
    except Exception as e:
        print('权限开启失败，' + str(e))


class MyWindow(QMainWindow, mainWindow.Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
