from math import pi
from time import perf_counter
from struct import unpack

class Sensors:
    def __init__(self,  can_bus = None,
                        angle_units = 'degrees',
                        length_units = 'mm',
                        torque_calib_data = {'mV/V': 1.4483,
                                        'tau_e': 32.1879,
                                        'gain': 717.6936123,
                                        'excitation': 10,
                                        'bias': 0.5}):
        if not can_bus:
            print("Provide can_bus as argument")
            self.__del__()
        
        self.protocol = {'encoders': b'\x01', 
                    'reset': b'\x02',
                    'config': b'\x03',
                    'torque': b'\x04', 
                    }

        self.sender = can_bus.send_bytes
        self.device_id = 0x01
        self.reciver = can_bus.recive_frame
        self.reply = 0

        self.t0 = perf_counter()
        self.t = 0

        self.angle = 0
        self.speed_angle = 0
        self.angle_units = angle_units

        self.lin = 0
        self.speed_lin = 0
        self.length_units = length_units

        self.torque_cd = torque_calib_data
        self.torque_voltage = 0
        self.torque = 0

        print("Sensors object was constructed.")
        
    
    def angle_unit_parser(self):
        (rot,) = unpack('h',self.reply[5:7])
        rot = rot / (1024. * 4.) # calibration
        if self.angle_units=="rad":
            angle = rot * 2 * pi
        else:
            angle = rot * 360.
        self.speed_angle=(angle - self.angle) / (self.t - self.t0)
        self.angle=angle

    def length_unit_parser(self):
        (lin,) = unpack('h',self.reply[2:4])
        lin = lin * (-1) * 25.4 / (360.0 * 4.0) # calibration
        if self.length_units=="m":
            length = lin * 10**(-3)
        else:
            length = lin
        self.speed_lin = (length - self.lin) / (self.t - self.t0)
        self.lin=length

    def read_encoders(self):
        message = self.protocol['encoders'] + 7*b'\x00'
        self.sender(self.device_id, message)
        _, _, self.reply = self.reciver()
        self.t = perf_counter()
        self.angle_unit_parser()
        self.length_unit_parser()
        self.t0 = self.t

    def read_voltage(self):
        message = self.protocol['torque'] + 7*b'\x00'
        self.sender(self.device_id, message)
        _, _, self.reply = self.reciver()
        (self.torque_voltage,) = unpack('f',self.reply[2:6])

    def calibration_torque(self):
        v = 0
        n = 1000
        for i in range(n):
            self.read_voltage()
            v += self.torque_voltage
        self.torque_cd['bias'] = v/n

    def read_torque(self):
        self.read_voltage()
        self.torque =   (self.torque_voltage - self.torque_cd['bias']) * self.torque_cd['tau_e'] / (self.torque_cd['excitation'] * self.torque_cd['mV/V'] * self.torque_cd['gain'])