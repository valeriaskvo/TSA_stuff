from can import CAN_Bus
from sensors import Sensors
from motors.gyems import GyemsDRC
from time import perf_counter, sleep
from multiprocessing import Process, Array, Lock, Value
import matplotlib.pyplot as plt
from math import cos, pi
import pandas as pd
# import numpy as np

RUN_TIME=10

TSA_stand = {'actuator_interface':'can1', 'id':0x148,                                   # actuator data
             'current_limit':1000, 'gains': {'kp':5.0, 'kd': 5.0},'control':'motor',    # control data 
                                                                                        # control types: 'motor' (default), 'linear_ee', 'rotational_ee'
             'amplitude':360,'period':10}                                                # trajectory parameters

def harmonic_trajectory(t,A=20,A0=None,T=5):
    if A0==None:
        A0=A
    return A0-A*cos(t*2*pi/T)

def pd_control(device,q_d,dq_d=0):
    data={}
    actuator=device['actuator']
    
    q, dq = actuator.state['angle'], actuator.state['speed']

    e, de = q_d - q, dq_d - dq
    
    i=actuator.state['current']
    i_d = device['gains']['kp']*e + device['gains']['kd']*de
    actuator.set_current(i_d)
    
    data['q_d']=q_d
    data['dq_d']=dq_d
    data['i_d']=i_d
    data['q']=q
    data['dq']=dq
    data['i']=i

    return data

def plot_results(t,y_d,y,y_label='Position [deg]',title='Position plot'):
    plt.plot(t,y_d,'r',label='Desired',linewidth=2.0)
    plt.plot(t,y,'b',label='Actual',linewidth=2.0)

    plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
    plt.grid(True)
    plt.legend()

    plt.xlabel('Time [sec]')
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(title+'.png')
    plt.clf()
    return

TSA_stand['actuator_bus'] = CAN_Bus(interface = TSA_stand['actuator_interface'])
TSA_stand['actuator'] = GyemsDRC(can_bus=TSA_stand['actuator_bus'], device_id=TSA_stand['id'])
TSA_stand['actuator'].set_degrees()
TSA_stand['actuator'].current_limit = TSA_stand['current_limit']
TSA_stand['actuator'].set_zero(persistant=True)
TSA_stand['actuator'].enable()

data = {'t':[], 'q_d':[], 'dq_d':[], 'i_d':[], 'q':[], 'dq':[], 'i':[]}
feedback_labels=['q_d','dq_d','i_d','q','dq','i']

t0=perf_counter()
t=0
try:
    while t<RUN_TIME:
        t=perf_counter()-t0
        q_d=harmonic_trajectory(t,A=TSA_stand['amplitude'],T=TSA_stand['period'])
        
        data_i=pd_control(TSA_stand,q_d)
        
        data['t'].append(t)
        for label in feedback_labels:
            data[label].append(data_i[label])

except KeyboardInterrupt:
    print("\nExit...")
    TSA_stand['actuator'].disable()

TSA_stand['actuator'].disable()
plot_results(data['t'],data['q_d'],data['q'],y_label='Position [deg]',title='Position')
plot_results(data['t'],data['dq_d'],data['dq'],y_label='Speed [deg/sec]',title='Speed')
plot_results(data['t'],data['i_d'],data['i'],y_label='Current [cu]',title='Current')

data=pd.DataFrame.from_dict(data)
data.to_csv("Experiment_result_c-"+TSA_stand['control']+".csv")
