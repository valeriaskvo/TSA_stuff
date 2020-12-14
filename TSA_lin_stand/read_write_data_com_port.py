import serial
import time

# port=port_list.comports()
s=serial.Serial("/dev/ttyACM0",baudrate=115200)

s.write(b"q")

time.sleep(3)

f = open('data_stand.csv', 'w')

s.write(b"w")
t0= time.time()
while(time.time()-t0<60):
    res=s.readline().decode('utf-8')
    f.write(res)

f.close()
s.write(b"q")