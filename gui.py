import pyqtgraph as pg
from PyQt5 import QtWidgets,QtCore,QtGui
from Ipmi import ipmi
import sys
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainUI, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.power_data_list  =[]
        self.x  = []

        self.graphWidget.setBackground('w')
        self.i0 = ipmi('10.10.10.10','ADMIN','ADMIN')
        self.i1 = ipmi('10.10.10.10','ADMIN','ADMIN')
        self.i2 = ipmi('10.10.10.10','ADMIN','ADMIN')
        self.i3 = ipmi('10.10.10.10','ADMIN','ADMIN')
        self.i4 = ipmi('10.10.10.10','ADMIN','ADMIN')
        self.i0.establish()
        self.i1.establish()
        self.i2.establish()
        self.i3.establish()
        self.i4.establish()
        self.graphWidget.setYRange(0, 4000, padding=0.01)
        self.txt = QtWidgets.QLabel(self.graphWidget)
        self.txt.setText('hellow')
        self.timer_start()
    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot_power)
        self.timer.start(100)
    def plot_power(self):
        if len(self.power_data_list) < 40:
            power = self.i0.get_power()+self.i1.get_power()+self.i2.get_power()+self.i3.get_power()+self.i4.get_power()
            self.txt.setText(str(power))
            self.power_data_list.append(power)
            self.x = list(range(len(self.power_data_list)))
            self.graphWidget.clear()
            self.graphWidget.plot(self.x,self.power_data_list,pen = 'r')
        else:
            del(self.power_data_list[0])
            power = self.i0.get_power()+self.i1.get_power()+self.i2.get_power()+self.i3.get_power()+self.i4.get_power()
            self.txt.setText(str(power))
            self.power_data_list.append(power)
            self.x = list(range(len(self.power_data_list)))
            self.graphWidget.clear()
            self.graphWidget.plot(self.x,self.power_data_list,pen = 'r')
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUI()
    gui.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
 