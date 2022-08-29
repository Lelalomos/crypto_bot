import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5 import QtWidgets
import cv2
import os

class Windows(QMainWindow):
    def __init__(self):
        super(Windows,self).__init__() 

        self.setFixedSize(300, 200)
        self.setWindowTitle("crypto")
        self.start_btn()
        self.stop_btn()
        self.plot_btn()
        self.show()

    def start_btn(self):
        self.start_var = QtWidgets.QPushButton(self)
        self.start_var.setText('Start')
        self.start_var.resize(self.start_var.minimumSizeHint())
        self.start_var.move(120,0)
        self.start_var.clicked.connect(self.on_clicked_start)

    def stop_btn(self):
        self.stop_var = QtWidgets.QPushButton(self)
        self.stop_var.setText('Stop')
        self.stop_var.move(120,50)
        self.stop_var.resize(self.stop_var.minimumSizeHint())
        self.stop_var.clicked.connect(self.on_clicked_stop)

    def plot_btn(self):
        self.combobox = QComboBox(self)
        self.combobox.addItems(['buy/sell','by-engine'])
        self.combobox.activated.connect(self.plot)
        self.combobox.move(100,100)
        self.combobox.resize(self.combobox.minimumSizeHint())

    def plot(self,index):
        print(f'plot: {index}')
        if str(index) == "1":
            img = cv2.imread(os.path.join(os.getcwd(),'images','image.png'))
            cv2.imshow('test',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def on_clicked_start(self):
        print('start')

    def on_clicked_stop(self):
        print('stop')
        

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    GUI = Windows()
    sys.exit(app.exec_())