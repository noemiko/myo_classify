# !/usr/bin/env python2

"""Module to send data from myo armband."""
from __future__ import print_function
from core import OSC
from core.myo_raw import MyoRaw

ip = "127.0.0.1"
port = 7111  # client where data are send
receiveIp = "127.0.0.1"
receivePort = 7125

m = MyoRaw()

client = OSC.OSCClient()
client.connect((ip, port))

server = OSC.OSCServer((receiveIp, receivePort))
server.timeout = 0


def proc_emg_osc(emg, moving):
    msg = OSC.OSCMessage()
    msg.setAddress("/myo/emg")
    msg.append(emg)
    sendOSC(msg)


def proc_imu_osc(quat, gyro, acc):
    msg = OSC.OSCMessage()
    msg.setAddress("/myo/imu")
    msg.append(quat)
    msg.append(gyro)
    msg.append(acc)
    sendOSC(msg)


def user_callback_vib(path, tags, args, source):
    m.vibrate(args[0])


def sendOSC(msg):
    print(msg)
    try:
        client.send(msg)
    except OSC.OSCClientError as error:
        print(error)
        print('ERROR: Client %s %i does not exist' % (client.address()[0], client.address()[1]))

m.connect()

m.add_emg_handler(proc_emg_osc)
m.add_imu_handler(proc_imu_osc)
server.addMsgHandler("/myo/vib", user_callback_vib)

try:
    while True:
        m.run(1)
        server.handle_request()
finally:
    m.disconnect()
    print()