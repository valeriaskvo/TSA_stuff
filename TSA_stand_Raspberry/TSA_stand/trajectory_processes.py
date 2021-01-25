import numpy as np
from collections import namedtuple
from time import perf_counter
from multiprocessing import Process, Array, Lock, Value

from can import CAN_Bus
from motors.gyems import GyemsDRC

# TODO:
#     * замерить частоту общения каждого процесса
#     * Вычислить, как быстро считается control
#     * Вычислить сколько длится Lock
#     * Обсудить, стоит ли вынести апдейт стейта движка
#     * Обсудить, как синхронить стейт мотора и стейт сенсоров
#     *
#     * Выяснить, причины, почему Семён считал время так как в изначальном коде
#       (device['state'][0] = perf_counter() - start)


# Global variables containers. Упрощённое объявление вместо *классов*
from sensors import Sensors

Gains = namedtuple('Gains', field_names='kp kd')
Motor = namedtuple('Motor', field_names='bus actuator gains state desired_value')
MySensors = namedtuple('MySensors', field_names='bus reader state')
# SystemParams = namedtuple('SystemParams', 'L0 R ...')

################# Params #################
trajectory_amplitude = 30
trajectory_period = 3

motor_bus = 'can0'
motor_id = 0x148
motor_limit = 1000

sensors_bus = 'can1'
sensors_id = 0x01  # nothing yet

################# Global variables ~ state #################
################# Initialization #################
motor_can_bus = CAN_Bus(interface=motor_bus)
actuator = GyemsDRC(can_bus=motor_can_bus, device_id=motor_id)
actuator.set_degrees()
actuator.current_limit = motor_limit
actuator.enable()

motor = Motor(bus=motor_can_bus, actuator=actuator,
              gains=Gains(kp=5.0, kd=5.0),
              state=Array('d', range(4)),
              desired_value=Value('d', 0))

sensors_can_bus = CAN_Bus(interface=sensors_bus, devices_id=sensors_id)
sensors_reader = Sensors(can_bus=sensors_can_bus)
sensors_reader.calibration_torque()
sensors = MySensors(bus=sensors_bus, reader=sensors_reader,
                    state=Array('d', range(4)))

start = perf_counter()


def write_to_motor(motor):
    """
    Using desired state, writes to motor desired state
    """

    actuator = motor.actuator
    state = motor.state  # Эта переменная имплементит интерфейс Lock класса
    try:
        while True:
            # IO-lock, due to actuator.state update
            actuator.set_current(motor.desired_value.value)

            # Лочим, чтобы атомарно записать новый стейт
            state.acquire()
            state[1] = actuator.state['angle']
            state[2] = actuator.state['speed']
            state[3] = actuator.state['torque']  # TODO: можно верить этой величине?
            state.release()

    except KeyboardInterrupt:
        actuator.disable()


def write_control(motor, sensors):
    """
    Infinitely and with minimum delay reads actual state variables:
        1. Theta, dTheta (from motor)
        2. X, dX (from sensors)
    Giving state, compute control and write desired value to motor (torque or amperage)
    """
    q, dq, i = 0, 0, 0
    e, de = 0, 0

    state = motor.state
    gains = motor.gains
    sensors = sensors.state

    # TODO: это норм, если стейт из сенсоров и от мотора могут приходить с разных
    #  отрезков времени?

    try:
        while True:
            # Read needed variables from sensors and motor
            # Motor
            state.acquire()
            _, q, dq, i = state
            state.release()
            ## Sensors
            # 1. Torque, Torque_voltage
            torque = sensors[0]
            torque_voltage = sensors[1]

            ## 2. X, dX, Angdle, dAngle
            # X = sensors[0]
            # dX = sensors[1]
            # angle = sensors[3]
            # dangle = sensors[4]

            # Find desired something
            # TODO: это можно вынести в if __name__ == '__main__':
            t = perf_counter() - start
            q_d, dq_d, ddq_d = trajectory(t, trajectory_period, trajectory_amplitude)

            # TODO: rewrite control
            # Control
            e, de = q_d - q, dq_d - dq
            motor.desired_value.value = gains.kp * e + gains.kd * de

    except KeyboardInterrupt:
        print('\nExiting write control....')


def read_sensors(sensors):
    reader = sensors.reader
    state = sensors.state
    try:
        while True:
            reader.read_torque()  # 1.
            # reader.read_encoders()    # 2.

            state.acquire()
            # 1. Torque
            state[0] = reader.torque
            state[1] = reader.torque_voltage
            ## 2. X, dX, Angdle, dAngle
            # state[0] = reader.lin
            # state[1] = reader.speed_lin
            # state[3] = reader.angle
            # state[4] = reader.speed_angle
            state.release()
    except KeyboardInterrupt:
        print('\nExiting reading sensors...')


def trajectory_sin(t, per=1, A=40):
    omega = 2 * np.pi / per
    phase = t * omega
    q = A * np.sin(phase)
    dq = omega * A * np.cos(phase)
    ddq = - omega ** 2 * A * np.sin(phase)
    return q, dq, ddq


if __name__ == '__main__':
    processes = []
    trajectory = trajectory_sin

    processes.append(Process(target=write_to_motor, args=(motor)))
    processes.append(Process(target=write_control, args=(motor, sensors)))
    processes.append(Process(target=read_sensors, args=(sensors)))

    print(f'\nProcesses are about to begin...\n ')
    for process in processes:
        process.start()

    q_d = 0
    data = {'t': [], 'q_d': [], 'q': [], 'dq': [], 'i': []}
    try:
        while True:
            while True:
                # q_d, dq_d, ddq_d = trajectory(t, 1, 30)
                # desired.value = [q_d, dq_d, ddq_d]

                data['q_d'].append(q_d)
                data['q'].append(motor.state[1])
                data['dq'].append(motor.state[2])
                data['i'].append(motor.state[3])

    finally:
        motor.actuator.disable()
