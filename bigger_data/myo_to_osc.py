"""Myo-to-OSC application.
Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000
basic on https://github.com/cpmpercussion/myo-to-osc
"""
from myo import *

import argparse
from datetime import datetime
from pythonosc import udp_client

parser = argparse.ArgumentParser(description='Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000.')
parser.add_argument('-a', '--address', dest='address', help='A Myo MAC address to connect to, in format "XX:XX:XX:XX:XX:XX".')

args = parser.parse_args()

osc_client = udp_client.SimpleUDPClient("localhost", 3002)  # OSC Client for sending messages.


def proc_imu(quat, acc, gyro):
    data_to_send = "acc,{0[0]},{0[1]},{0[2]},gyro,{1[0]},{1[1]},{1[2]},quat,{2[0]},{2[1]},{2[2]},{2[3]},{3}"\
        .format(acc, gyro, quat, datetime.now().isoformat())
    print(data_to_send)
    osc_client.send_message("/imu", data_to_send)


def proc_emg(emg_data):
    data_to_send = "emg,{0[0]},{0[1]},{0[2]},{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{1}"\
        .format(emg_data, datetime.now().isoformat())
    print(data_to_send)
    osc_client.send_message("/emg", data_to_send)


def proc_battery(battery_level):
    # print("Battery", battery_level, end='\r')
    osc_client.send_message("/battery", battery_level)

if args.address is not None:
    print("Attempting to connect to Myo:", args.address)
else:
    print("No Myo address provided.")

# Setup Myo Connection
# m = Myo()  # scan for USB bluetooth adapter and start the serial connection automatically
# m = Myo(tty="/dev/tty.usbmodem1")  # MacOS
m = Myo(tty="/dev/ttyACM0")  # Linux
m.add_emg_handler(proc_emg)
m.add_imu_handler(proc_imu)
m.add_battery_handler(proc_battery)


m.connect(address=args.address)  # connects to specific Myo unless arg.address is none.
# Setup Myo mode, buzzes when ready.
m.sleep_mode(Sleep_Mode.never_sleep.value)
# EMG and IMU are enabled, classifier is disabled (thus, no sync gestures required, less annoying buzzing).
m.set_mode(EMG_Mode.send_emg.value, IMU_Mode.send_data.value, Classifier_Mode.disabled.value)
# Buzz to show Myo is ready.
m.vibrate(1)

def run_loop():
    m.run()

print("Now running...")
try:
    while True:
        run_loop()
except KeyboardInterrupt:
    pass
finally:
    m.disconnect()
    print("\nDisconnected")


# TODO:
#   - move classification if then to myohw.py
#   - experiment connecting to multiple myos.
