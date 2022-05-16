import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtWidgets
from cypto import main, stop_service

class Windows(QMainWindow):
    def __init__(self):
        super(Windows,self).__init__()
        # self.setGeometry(50, 50)
        self.setFixedSize(300, 100)
        self.setWindowTitle("crypto")
        self.start_btn()
        self.stop_btn()
        self.show()
        # self.show()

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

    def on_clicked_start(self):
        main()

    def on_clicked_stop(self):
        stop_service()
        

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    GUI = Windows()
    sys.exit(app.exec_())