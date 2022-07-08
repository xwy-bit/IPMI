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
        self.setWindowTitle('PSU Curve')
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.power_data_list  =[]
        self.x  = []

        self.graphWidget.setBackground('w')
        self.i0 = ipmi('','','')
        self.i1 = ipmi('','','')
        self.i2 = ipmi('','','')
        self.i3 = ipmi('','','')
        self.i4 = ipmi('','','')
        self.i0.establish()
        self.i1.establish()
        self.i2.establish()
        self.i3.establish()
        self.i4.establish()
        self.graphWidget.setYRange(500, 1000, padding=0.01)
        self.txt = QtWidgets.QLabel(self)
        self.txt.setText('hellow')
        self.txt.setStyleSheet("color: blue")
        self.txt.setFont(QtGui.QFont('Arial', 20))
        self.txt.move(300,30)
        self.txt0 = QtWidgets.QLabel(self)
        self.txt0.setText('hellow')
        self.txt0.setStyleSheet("color: green")
        self.txt0.move(100,200)
        self.txt1 = QtWidgets.QLabel(self)
        self.txt1.setText('hellow')
        self.txt1.setStyleSheet("color: green")
        self.txt1.move(200,200)
        self.txt2 = QtWidgets.QLabel(self)
        self.txt2.setText('hellow')
        self.txt2.setStyleSheet("color: green")
        self.txt2.move(300,200)
        self.txt3 = QtWidgets.QLabel(self)
        self.txt3.setText('hellow')
        self.txt3.setStyleSheet("color: green")
        self.txt3.move(400,200)
        self.txt4 = QtWidgets.QLabel(self)
        self.txt4.setText('hellow')
        self.txt4.setStyleSheet("color: green")
        self.txt4.move(500,200)
        self.timer_start()
    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot_power)
        self.timer.start(1)
    def plot_power(self):
        if len(self.power_data_list) < 40:
            p0 = self.i0.get_power()
            p1 = self.i1.get_power()
            p2 = self.i2.get_power()
            p3 = self.i3.get_power()
            p4 = self.i4.get_power()
            self.txt0.setText('i0: '+str(p0))
            self.txt1.setText('i1: '+str(p1))
            self.txt2.setText('i2: '+str(p2))
            self.txt3.setText('i3: '+str(p3))
            self.txt4.setText('i4: '+str(p4))
            power = p0+p1+p2+p3+p4
            self.txt.setText(str(power))
            self.power_data_list.append(p4)
            self.x = list(range(len(self.power_data_list)))
            self.graphWidget.clear()
            self.graphWidget.plot(self.x,self.power_data_list,pen = 'r')
        else:
            del(self.power_data_list[0])
            p0 = self.i0.get_power()
            p1 = self.i1.get_power()
            p2 = self.i2.get_power()
            p3 = self.i3.get_power()
            p4 = self.i4.get_power()
            self.txt0.setText('i0: '+str(p0))
            self.txt1.setText('i1: '+str(p1))
            self.txt2.setText('i2: '+str(p2))
            self.txt3.setText('i3: '+str(p3))
            self.txt4.setText('i4: '+str(p4))
            power = p0+p1+p2+p3+p4
            self.txt.setText(str(power))
            self.power_data_list.append(p4)
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
 