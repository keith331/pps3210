import sys
import time
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
import serial.tools.list_ports
import serial
from threading import Thread

from ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if not self.initialize_dev():
            self.show_msgbox('No devices found')
            sys.exit()

        self.volt_ch = {'CH1':'VOLTAGE1','CH2':'VOLTAGE2','CH3':'VOLTAGE3'}
        self.curr_ch = {'CH1':'CURRENT1','CH2':'CURRENT2','CH3':'CURRENT3'}
        self.setup_control()

    def setup_control(self):
        pass
        
        self.ui.pushButton_2.clicked.connect(self.set_voltage)
        self.ui.pushButton_3.clicked.connect(self.set_current)
        self.ui.pushButton_4.clicked.connect(self.connect_to_device)
        self.ui.pushButton.clicked.connect(self.power)

    def initialize_dev(self):
        
        ports = serial.tools.list_ports.comports()
        # self.ui.comboBox_2.clear()
        if ports is not None:
            for p in ports:
                self.ui.comboBox_2.addItem(p.device)
                return True

    def set_voltage(self):

        val = float(self.ui.lineEdit.text())
        val = round(val,3)
        val = str(val)
        ch = self.volt_ch[self.ui.comboBox.currentText()]
        cmd = ch + ' ' + val + '\n'
        
        self.conn = serial.Serial(port=self.ui.comboBox_2.currentText(),baudrate=9600)
        self.conn.write(cmd.encode())
        self.conn.close()

        self.connect_to_device()

    def set_current(self):

        val = float(self.ui.lineEdit.text())
        val = round(val,4)
        val = str(val)
        ch = self.curr_ch[self.ui.comboBox.currentText()]
        cmd = ch + ' ' + val + '\n'
        
        self.conn = serial.Serial(port=self.ui.comboBox_2.currentText(),baudrate=9600)
        self.conn.write(cmd.encode())
        self.conn.close()

        self.connect_to_device()

    def show_msgbox(self, text):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Confirm')
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def connect_to_device(self):
        
        self.conn = serial.Serial(port=self.ui.comboBox_2.currentText(),baudrate=9600)

        self.conn.write(b'VOLTAGE1?\n')
        ch1 = 'CH1   ' + self.conn.readline().decode('ascii').rstrip() + '  '
        self.conn.write(b'CURRENT1?\n')
        ch1 += self.conn.readline().decode('ascii').rstrip()        
        time.sleep(.2)
        self.conn.write(b'VOLTAGE2?\n')
        ch2 = 'CH2   ' + self.conn.readline().decode('ascii').rstrip() + '  '
        self.conn.write(b'CURRENT2?\n')      
        ch2 += self.conn.readline().decode('ascii').rstrip()         
        time.sleep(.2)
        self.conn.write(b'VOLTAGE3?\n')
        ch3 = 'CH3   ' + self.conn.readline().decode('ascii').rstrip() + '  '
        self.conn.write(b'CURRENT3?\n')      
        ch3 += self.conn.readline().decode('ascii').rstrip() 
        volt_all = ch1 + '\n' + ch2 + '\n' + ch3
        self.ui.textEdit.setText(volt_all)
        self.conn.close()

    def power(self):

        self.conn = serial.Serial(port=self.ui.comboBox_2.currentText(),baudrate=9600)
        if self.ui.pushButton.isChecked():
            # self.ui.pushButton.setStyleSheet('background-color: #de5f2d')
            self.ui.pushButton.setStyleSheet('''
                        QPushButton::checked
                        {
                            background-color: #de5f2d
                        }
                        ''')
            self.conn.write(b'OUT:ALL ON\n')
            self.conn.close()
        else:
            self.ui.pushButton.setStyleSheet('background-color: #75b2ae')
            self.conn.write(b'OUT:ALL OFF\n')
            self.conn.close()    

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())  
    
if __name__ == '__main__':

    runapp = Thread(target=main)
    runapp.start()
    runapp.join()