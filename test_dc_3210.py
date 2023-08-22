import serial
import time

time.sleep(5)
conn = serial.Serial(port='COM6',baudrate=9600)
conn.write(b'VSET 2\n')
conn.write(b'OUT:ALL ON\n')
conn.write(b'BEEP 0\n')
conn.write(b'TIMER 00:00:07\n')
conn.write(b'TIMER ON\n')
conn.close()



