from can import CAN_Bus
from time import perf_counter
from time import sleep
from struct import unpack
from sensors import Sensors

def from_bytes(byte_string, signed = False):
    return int.from_bytes(byte_string, byteorder='little', signed = signed)


def to_bytes(n, integer, signed = True):
    return int(integer).to_bytes(n, byteorder='little', signed = signed)

  

protocol = {'read_data': b'\x01', 
            'reset': b'\x02',
            'torque': b'\x04', 
            }

bus = CAN_Bus(interface = 'can1')
device_id = 0x01

sens = Sensors(can_bus = bus)

try:
    sens.calibration_torque()
    print(sens.torque_cd['bias'])
    while True:
        sens.read_torque()
        print(sens.torque_voltage,sens.torque)

        # message = protocol['torque'] + 7*b'\x00'
        # bus.send_bytes(device_id, message)
        # canid, dlc, reply = bus.recive_frame()
        # # print(reply)
        
        # (x,) = unpack('f',reply[2:6])
        # print(x)

        # message = protocol['read_data'] + 7*b'\x00'
        # bus.send_bytes(device_id, message)
        # canid, dlc, reply = bus.recive_frame()
        # (data_1,) = unpack('h',reply[2:4])
        # (data_2,) = unpack('h',reply[5:7])
        # print(data_1,data_2)

        # sleep(0.08)


        # # message = protocol['motor_on'] + 7*b'\x00'
        # message = protocol['read_data']  + 7*b'\x00'
        # # print(message)

        # bus.send_bytes(device_id, message)
        # canid, dlc, reply = bus.recive_frame()
        # # state = parse_sensor_data(reply)
        # # dt = perf_counter() - t
        # # vel = ((state['motor_counts']-512) - pos)/dt
        # # pos = state['motor_counts']-512

        # print(from_bytes(reply[2:4]),from_bytes(reply[5:7]))
        # # control = 1*pos + 0.05*vel  
        # # t = perf_counter()
        # # print(reply[1:3])
        # # print()

    
except KeyboardInterrupt:
    # message = protocol['motor_off'] + 7*b'\x00'
    #     # message = protocol['set_current'] + 7*b'\x00'
    # bus.send_bytes(device_id, message)
    # canid, dlc, reply = bus.recive_frame()
    bus.can_reset()
# except:
#     bus.can_reset()