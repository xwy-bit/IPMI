# file: combobox.py
#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

This example shows how to use
a QComboBox widget.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from Ipmi import ipmi
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QApplication,
    QPushButton,
    QMainWindow,
    QLineEdit,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
)
from PyQt6 import QtGui, QtCore
import pyqtgraph as pg
from qt_material import apply_stylesheet


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(400, 400, 850, 500)

        self.machine_files = "config.csv"
        self.machine_info = []
        self.machine_count = 0
        self.machine_selected_label = []
        self.machine_selected = []
        self.machines = []

        self.timer = QtCore.QTimer(self)
        self.graphWidget = pg.PlotWidget()

        self.power_index = 0
        self.power_data = []
        self.power_max = -1

        self.interval = 1000
        self.maxtime = 60

        self.initUI()
        self.show()

    def initUI(self):
        # define basic items
        self.reset_button = QPushButton("Start")
        self.load_button = QPushButton("Load Config")
        self.interval_text = QLineEdit("1000")
        self.maxtime_text = QLineEdit("60")
        self.interval_label = QLabel("Interval (ms): ")
        self.maxtime_label = QLabel("Max Time (s): ")
        self.graphWidget.setYRange(0, 4000, padding=0.01)
        self.current_power_label1 = QLabel("Current Label = ")
        self.current_power_label1.setStyleSheet("font-size:15pt;")
        self.current_power_label2 = QLabel("-1")
        self.current_power_label2.setStyleSheet("font-weight: bold; color: green; font-size:20pt;")
        self.max_power_label1 = QLabel("Max Power = ")
        self.max_power_label1.setStyleSheet("font-size:15pt;")
        self.max_power_label2 = QLabel("-1")
        self.max_power_label2.setStyleSheet("font-weight: bold; color: red; font-size:20pt;")

        # set item size
        self.reset_button.setMaximumWidth(100)
        self.interval_text.setMaximumWidth(150)
        self.maxtime_text.setMaximumWidth(150)
        self.graphWidget.setMinimumWidth(800)
        self.graphWidget.setMinimumHeight(600)

        # set layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.addWidget(self.reset_button, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.load_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.interval_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.maxtime_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.interval_text, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.maxtime_text, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.graphWidget, 0, 2, 10, 10)
        self.grid_layout.addWidget(self.current_power_label1, 8, 0, 1, 1)
        self.grid_layout.addWidget(self.current_power_label2, 8, 1, 1, 1)
        self.grid_layout.addWidget(self.max_power_label1, 9, 0, 1, 1)
        self.grid_layout.addWidget(self.max_power_label2, 9, 1, 1, 1)
        self.setLayout(self.grid_layout)

        # connect items
        self.load_button.clicked.connect(self.load_machine)
        self.reset_button.clicked.connect(self.reset_machine)
        self.timer.timeout.connect(self.plot_power)
        self.interval_text.textChanged[str].connect(self.update_interval)
        self.maxtime_text.textChanged[str].connect(self.update_maxtime)

        self.load_machine()

    def load_machine(self):
        self.clear_layout(self.grid_layout)
        self.machine_files = "config.csv"
        self.machine_info = []
        self.machine_count = 0
        self.machine_selected_label = []
        self.machine_selected = []
        self.machines = []
        with open(self.machine_files, "r") as f:
            for line in f.readlines():
                info = line.strip().split(",")
                machine_name = info[0]
                machine_ip = info[1]
                machine_username = info[2]
                machine_password = info[3]
                self.machine_count += 1
                self.machine_info.append(
                    (machine_name, machine_ip, machine_username, machine_password)
                )

        # update layout
        self.grid_layout.setSpacing(10)
        max_grid_size = max(10, 1 + 1 + 1 + 1 + self.machine_count)
        self.grid_layout.addWidget(self.reset_button, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.load_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.interval_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.maxtime_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.interval_text, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.maxtime_text, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.graphWidget, 0, 2, max_grid_size, max_grid_size)
        self.grid_layout.addWidget(self.current_power_label1, max_grid_size - 2, 0, 1, 1)
        self.grid_layout.addWidget(self.current_power_label2, max_grid_size - 2, 1, 1, 1)
        self.grid_layout.addWidget(self.max_power_label1, max_grid_size - 1, 0, 1, 1)
        self.grid_layout.addWidget(self.max_power_label2, max_grid_size - 1, 1, 1, 1)

        item_index = 0
        for item in self.machine_info:
            (machine_name, machine_ip, machine_username, machine_password) = item
            check_box = QCheckBox(machine_name, self)
            check_box.stateChanged.connect(self.reset_system)
            self.machine_selected.append(check_box)
            self.grid_layout.addWidget(check_box, item_index + 3, 0, 1, 2)
            item_index += 1
        

        # update size
        self.reset_button.setMaximumWidth(100)
        self.interval_text.setMaximumWidth(150)
        self.maxtime_text.setMaximumWidth(150)
        self.graphWidget.setMinimumWidth(800)
        self.graphWidget.setMinimumHeight(600)
        self.grid_layout.update()


    def update_interval(self, text):
        self.timer.stop()
        self.reset_button.setText("Start")
        self.power_index = 0
        self.power_data = []
        self.interval = int(text)
        self.power_max = -1
        self.current_power_label2.setText("0")
        self.max_power_label2.setText("0")

    def update_maxtime(self, text):
        self.timer.stop()
        self.reset_button.setText("Start")
        self.power_index = 0
        self.power_data = []
        self.maxtime = int(text)
        self.power_max = -1
        self.current_power_label2.setText("0")
        self.max_power_label2.setText("0")

    def reset_system(self):
        self.timer.stop()
        self.reset_button.setText("Start")
        self.power_index = 0
        self.power_data = []
        self.power_max = -1
        self.current_power_label2.setText("0")
        self.max_power_label2.setText("0")

    def reset_machine(self):
        self.interval_text.setText(str(self.interval))
        self.maxtime_text.setText(str(self.maxtime))
        self.power_data = []
        self.power_index = 0
        self.reset_button.setText("Reset")
        self.current_power_label2.setText("Connecting ...")
        self.max_power_label2.setText("Connecting ...")
        self.power_max = -1
        index = 0
        self.machines = []
        # print(self.machine_info)
        for item in self.machine_selected:
            if item.isChecked():
                name, ip, username, password = self.machine_info[index]
                machine_item = (ipmi(ip, username, password))
                machine_item.establish()
                self.machines.append(machine_item)
            index += 1
        self.timer_start()

    def clear_layout(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())):
                widgetToRemove = layout.itemAt(i).widget()
                # remove it from the layout list
                layout.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)

    def timer_start(self):
        self.timer.start(1)
        self.timer.setInterval(self.interval)

    def plot_power(self):
        current_power = 0
        for machine in self.machines:
            current_power += machine.get_power()
        self.power_data.append(current_power)
        self.power_max = max(current_power, self.power_max)

        item_counts = int(self.maxtime * 1000 / self.interval)
        while len(self.power_data) > item_counts:
            del self.power_data[0]
        if len(self.power_data) > item_counts:
            self.x = list(range(item_counts))
        else:
            self.x = list(range(len(self.power_data)))
        self.current_power_label2.setText(str(current_power))
        self.max_power_label2.setText(str(self.power_max))

        self.graphWidget.clear()
        self.graphWidget.plot(self.x, self.power_data, pen="g")


def main():
    app = QApplication(sys.argv)
    ex = Dashboard()
    apply_stylesheet(app, theme="dark_teal.xml")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
