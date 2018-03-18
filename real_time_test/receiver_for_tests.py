# adapted from:
# https://github.com/ptone/pyosc/blob/master/examples/knect-rcv.py
# !/usr/bin/env python3

from core.OSC import OSCServer
from real_time_models_test import ModelTester
# default settings

ip = "localhost"
port = 7112

server = OSCServer((ip, port))
server.timeout = 0
run = True
tester = ModelTester()

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


# funny python's way to add a method to an instance of a class
import types

server.handle_timeout = types.MethodType(handle_timeout, server)


def user_callback_imu(path, tags, args, source):
    orientation = args[:3]
    gyroscope = args[3:6]
    acceleration = args[6:]
    tester.get_data(dict(quat=orientation, gyro=gyroscope, acc=acceleration))


def user_callback_emg(path, tags, args, source):
    tester.get_data(dict(emg=args))

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False


server.addMsgHandler("/myo/imu", user_callback_imu)
server.addMsgHandler("/myo/emg", user_callback_emg)
server.addMsgHandler( "/quit", quit_callback)

while run:
    server.handle_request()

if __name__ == '__main__':
    import sys

server.close()