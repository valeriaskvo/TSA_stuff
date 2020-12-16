import serial
import time

s=serial.Serial("/dev/ttyACM0",baudrate=115200)

s.write(b"q")

time.sleep(3)

f = open('data_stand_1.csv', 'w')

s.write(b"w")
t0= time.time()
while(time.time()-t0<40):
    res=s.readline().decode('utf-8')
    f.write(res)

f.close()
s.write(b"q")