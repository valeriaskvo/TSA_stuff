from math import pi
from time import perf_counter

class Sensors:
    def __init__(self, can_bus=None, angle_units='degrees',length_units='mm'):
        if not can_bus:
            print("Provide can_bus as argument")
            self.__del__()
        self.reciver = can_bus.recive_frame
        self.t0 = perf_counter()
        self.t = 0
        self.angle = 0
        self.speed_angle = 0
        self.angle_units = angle_units
        self.lin = 0
        self.speed_lin = 0
        self.length_units = length_units
        self.reply = 0
    
    def angle_unit_parser(self):
        rot = int.from_bytes(self.reply[4:], byteorder='little', signed = True)/(1024.*4.)
        if self.angle_units=="rad":
            angle = rot*2*pi
        else:
            angle = rot*360.
        self.speed_angle=(angle-self.angle)/(self.t-self.t0)
        self.angle=angle

    def length_unit_parser(self):
        lin = int.from_bytes(self.reply[:4], byteorder='little', signed = True)*(-1)*25.4/(360.0*4.0)
        if self.length_units=="m":
            length = lin*10**(-3)
        else:
            length = lin
        self.speed_lin=(length-self.lin)/(self.t-self.t0)
        self.lin=length

    def recieve_data(self):
        _,_, self.reply = self.reciver()
        self.t = perf_counter()
        self.angle_unit_parser()
        self.length_unit_parser()
        self.t0 = self.t


