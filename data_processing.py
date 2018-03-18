import csv
import os

scisors_training_set = []
paper_training_set = []
stone_training_set = []


def process_from_files():
    data_folder = 'data'
    for root, dirs, files in os.walk(data_folder, topdown=False):
        for name in files:
            if root == "{}/paper1".format(data_folder):
                file_as_list = read_parsed_data(root, name)
                paper_training_set.append(file_as_list)
            elif root == "{}/scisors".format(data_folder):
                file_as_list = read_parsed_data(root, name)
                scisors_training_set.append(file_as_list)
            elif root == "{}/stone".format(data_folder):
                file_as_list = read_parsed_data(root, name)
                stone_training_set.append(file_as_list)
    return stone_training_set, paper_training_set, scisors_training_set


def read_parsed_data(root, name):
    file_path = os.path.join(root, name)
    print("Opening file:", file_path)
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        parsed_file = parse_different_sensors_to_one_row(reader)
    return change_dict_to_list(parsed_file)


def change_dict_to_list(parsed_data_to_dict):
    row_of_one_learning_row = []
    for row in parsed_data_to_dict:
        for v in row.values():
            row_of_one_learning_row.extend(v)
    return row_of_one_learning_row


def parse_different_sensors_to_one_row(file_rows):
    """
    File contain sensor data in two rows with format:
    "2018-03-18 14:13:06.380920","emg","45","82","113","142","59","40","30","34"
    "2018-03-18 14:13:06.388565","acc","720","204","-96","33","gyro","6208","-194","-1945","quat","-12062","7837","-4796"
    Needed is parse it to one row and change to dict for easier later parse.
    :param file_rows: list of lists that containt sensors data
    :return example:
    [{emg:[1,2,4], acc:[12,12,12,12], gyro:[12,2,3], quat:[1,2,3],{(...)}]
    """
    rows = []
    sensors = dict()

    for row in file_rows:
        if "emg" in sensors and "acc" in sensors:
            rows.append(sensors)
            sensors = dict()
        if row[1] == "emg":
            sensors["emg"] = row[2:10]
        else:
            sensors["acc"] = row[2:6]
            sensors["gyro"] = row[7:10]
            sensors["quat"] = row[11:15]
    if len(rows) == 50:
        rows.pop(0)
    return rows


if __name__ == "__main__":
    process_from_files()
    print(len(paper_training_set[0]))