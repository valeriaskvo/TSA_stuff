import serial
import serial.tools.list_ports as port_list

# port=port_list.comports()
s=serial.Serial("/dev/ttyACM0",baudrate=115200)
f = open('data_stand.csv', 'w')

for i in range(10):
    res=s.readline().decode('utf-8')
    print(res)
    f.write(res)

f.close()


