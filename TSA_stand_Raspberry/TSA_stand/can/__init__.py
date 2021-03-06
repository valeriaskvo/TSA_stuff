import socket
import struct
import os


# TODO: 
# Add support of python-can lib 
# Add different hardware devices
#       can-hacker
#       



class CAN_Bus:
    def __init__(self, interface = 'can0', devices_id = [0x001], serial_port = None, device = None, bitrate = 1000000):
        
        self.frame_format = "=IB3x8s"
        self.frame = 0
        self.interface = interface
        self.bitrate = bitrate
        self.devices_reply = dict()
        # self.messages = dict()
        self.id = devices_id

        self.can_down()
        self.can_set()
        if serial_port or device == 'can_hacker':
            self.can_hacker_init(port = serial_port, baud_rate = 115200)
        self.can_up()

        self.socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.socket.bind((self.interface, ))


    def __del__(self):
        self.can_down()
        print('CAN Devices object was destructed')
        

    def can_hacker_init(self, port = None, baud_rate = 115200):
        if not port:
            port = 'ttyACM0'
            print(f'<port> argument is not provided and choosen to be /dev/{port}')
        # self.can_down()
        self.serial_port = '/dev/' + port
        # os.system(f'sudo slcand -o -c -s8 -S {baud_rate} {serial_port} {interface}')
        # TODO:
        # Implent different speeds

        os.system(f'sudo slcand -o -c -s8 -S {baud_rate} {self.serial_port} {self.interface}')
        print(f'CAN device is connected on {port} / {baud_rate} and up as interface <{self.interface}> with {self.bitrate} bps')


    def can_set(self):
        os.system(f'sudo ip link set {self.interface} type can bitrate {self.bitrate}')
        print(f'CAN interface <{self.interface}> is setted on {self.bitrate} bps')


    def can_down(self):
        os.system(f'sudo ifconfig {self.interface} down')
        print(f'CAN interface <{self.interface}> is down')


    def can_up(self):
        os.system(f'sudo ifconfig {self.interface} up')
        os.system(f'sudo ifconfig {self.interface} txqueuelen 65536')
        print(f'CAN interface <{self.interface}> is up')

    def can_reset(self):
        '''Reset the CAN interface'''
        self.can_down()
        self.can_set()
        self.can_up()
        print(f'CAN interface <{self.interface}> was reseted')


    def build_can_frame(self, can_id, data):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack(self.frame_format, can_id, can_dlc, data)


    def parse_can_frame(self, frame):
        can_id, can_dlc, data = struct.unpack(self.frame_format, frame)
        return (can_id, can_dlc, data[:can_dlc])


    def send_bytes(self, can_id, bytes_to_send):
        self.frame = self.build_can_frame(can_id, bytes_to_send)
        self.socket.send(self.frame)


    def recive_frame(self):
        self.r_msg, _ = self.socket.recvfrom(16)
        can_id, can_dlc, can_data = self.parse_can_frame(self.r_msg)
        return can_id, can_dlc, can_data

    def send_recv(self, messages):
        'Send/recive routine'
        for device_id in self.id:
            self.send_bytes(device_id, messages[device_id])    
            can_id, can_dlc, can_data = self.recive_frame()
            self.devices_reply[device_id] = can_data
        
        # for device_id in self.id:
        #     self.send_bytes(device_id, messages[device_id])    
        
        # for device_id in self.id:
        #     can_id, can_dlc, can_data = self.recive_reply()
        #     self.devices_reply[can_id] = can_data

        return self.devices_reply

    def send_recive_threads(self, messages):
        # TODO: separate threads/processes for send and recive 
        # possibly separate hardware interfaces 
        pass
