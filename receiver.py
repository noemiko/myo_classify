# adapted from:
# https://github.com/ptone/pyosc/blob/master/examples/knect-rcv.py
import csv
import time
from datetime import datetime

from core.OSC import OSCServer


class Saver(object):

    def __init__(self):
        self.server = ""
        self.all_data = []
        self.timer_2sec = ''
        self.file_name = ""
        self.ip = "localhost"
        self.port = 7111  # port which one this listener wait for data
        self.file_counter = 0

    def start_new_record(self):
        print(" Ready?")
        name = raw_input("Give me file name/n")
        self.file_name = str(datetime.now()) + name
        raw_input("Press Enter to continue...")
        self.all_data = []
        self.timer_2sec = time.time() + 2
        self.start_server_to_listen(self.user_callback_imu, self.user_callback_emg)

    def save_raw_data(self, myo_data):
        """
        :param myo_data: dict
        :return:
        """
        # print("received",datetime.now())
        # print(myo_data)

        row = self.get_dict_as_list_with_timestamp(myo_data)
        self.all_data.append(row)
        if time.time() >= self.timer_2sec:
            new_file_name = "["+str(self.file_counter)+"]"+self.file_name + ".csv"

            with open("./data/"+new_file_name, 'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
                for row in self.all_data:
                    spamwriter.writerow(row)
            print("Created new file", new_file_name)
            self.server.close()
            self.all_data = []
            self.start_new_record()

    def get_dict_as_list_with_timestamp(self, myo_data):
        """
        Change dict like {yolo:[123,345]}
        to list timestamp, yolo, 123, 345
        :param myo_data:
        :return:
        """
        row = [str(datetime.now()),]
        for key, sensor_data in myo_data.items():
            row.append(key)
            row.extend(sensor_data)
        return row

    def user_callback_imu(self, path, tags, args, source):
        print(args)
        orientation = args[:3]
        gyroscope = args[3:6]
        acceleration = args[6:]
        saver.save_raw_data(dict(quat=orientation, gyro=gyroscope, acc=acceleration))

    def user_callback_emg(self, path, tags, args, source):
        print(args)
        saver.save_raw_data(dict(emg=args))

    def start_server_to_listen(self, imu_handler, emg_handler):
        self.file_counter += 1
        self.server = OSCServer((self.ip, self.port))
        self.server.timeout = 0
        self.server.addMsgHandler("/myo/imu", imu_handler)
        self.server.addMsgHandler("/myo/emg", emg_handler)
        self.server.serve_forever()


saver = Saver()
saver.start_new_record()

