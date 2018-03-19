"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
from datetime import datetime
import csv
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


class Saver(object):

    def __init__(self):
        self.server = ""
        self.all_data = []
        self.timer_2sec = ''
        self.file_name = ""
        self.ip = "127.0.0.1"
        self.port = 3002  # port which one this listener wait for data
        self.file_counter = 0

    def start_new_record(self):
        print(" Ready?")
        name = input("Give me file name/n")
        self.file_name = str(datetime.now()) + name
        input("Press Enter to continue...")
        self.all_data = []
        self.timer_2sec = time.time() + 2
        self.start_server_to_listen(self.user_callback_imu, self.user_callback_emg)

    def save_raw_data(self, myo_data):
        row = self.change_string_to_list(myo_data)
        self.all_data.append(row)
        if time.time() >= self.timer_2sec:
            new_file_name = "["+str(self.file_counter)+"]"+self.file_name + ".csv"

            with open("./data/"+new_file_name, 'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
                for row in self.all_data:
                    spamwriter.writerow(row)
            print("Created new file", new_file_name)
            self.server.server_close()
            self.all_data = []
            self.start_new_record()

    def change_string_to_list(self, myo_data):
        """
        Change string separated with delimiter
        to list with timestamp[2018-03-19T23:03:47.100725, yolo, 123, 345]
        """
        raw_data = myo_data.split(",")
        raw_data.insert(0, datetime.now().isoformat())
        return raw_data

    def user_callback_imu(self, address_come_from, args):
        self.save_raw_data(args)

    def user_callback_emg(self, address_come_from, args):
        self.save_raw_data(args)

    def start_server_to_listen(self, imu_handler, emg_handler):
        self.file_counter += 1
        dispatcher = Dispatcher()
        dispatcher.map("/imu", imu_handler)
        dispatcher.map("/emg", emg_handler)
        self.server = osc_server.OSCUDPServer((self.ip, self.port), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()

Saver().start_new_record()
