# This Python file uses the following encoding: utf-8
from mainwindow import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *

import sys
import psutil
import time


# class MainUiClass(QtGui.QMainWindow, Ui_MainWindow):
#     def __init__(self, parent = None):
#         super(MainUiClass, self).__init__(parent)
#         self.setupUi(self)
#             

class Communicate(QObject):
    updateCpu = Signal(int)

    # def __init__(self, window):
    #     super(QObject, self).__init__()
    #     self.window = window
    #     self.window.update_cpu_usage.connect(self.window.updateProgressBar, False)

        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.threadclass = ThreadClass()
        self.threadclass.setWindow(self)
        self.threadclass.start()
        
        self.c = Communicate()
        self.c.updateCpu.connect(self.update_cpu_usage)

    def update_cpu_usage(self, val):
        self.ui.progressBar.setValue(val)
        # self.update.emit(True)
        # self.ui.next_btn.clicked.connect(self.next)
        


class ThreadClass(QThread, QMainWindow):
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)
        
    def setWindow(self, window):
        self.window = window
        
    def run(self):
        while True:
            usage = psutil.cpu_percent()
            self.window.c.updateCpu.emit(usage)
            
            # self.c.updateCpu.connect(self.update_cpu_usage, usage)
            time.sleep(2)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # controller = WorkerSignals(window)
    window.show()
    sys.exit(app.exec_())