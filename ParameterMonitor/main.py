import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import mainWindow

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class MyWindow(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
