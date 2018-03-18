import pickle
from ..data_processing import change_dict_to_list


class ModelTester(object):
    all_data = []
    timer_2sec = ''
    points = 1
    name = ""

    def get_data(self, myo_data):
        """
        :param myo_data: dict
        :return:
        """
        if self.all_data == []:
            self.all_data.append(myo_data)
        else:
            if len(self.all_data[-1].keys()) == 4:
                self.all_data.append(myo_data)
            else:
                if myo_data.keys()[0] not in self.all_data[-1].keys():
                    self.all_data[-1].update(myo_data)

        if len(self.all_data) >= 50:
            parsed_hand_move = change_dict_to_list(self.all_data)

            if len(parsed_hand_move) > 882:
                number_data_to_remove = len(parsed_hand_move) - 882
                del parsed_hand_move[-number_data_to_remove:]
            self.all_data = []
            models_root = "models/"
            ada_model_file = 'ada_model.sav'
            forest_model_file = 'forest_model.sav'
            forest_model_est_25_file = 'forest_est_25_model.sav'
            svm_model_file = 'svm_model.sav'
            bagging_model_file = 'bagging_model.sav'
            extra_tree_model_file = 'extra_tree_model.sav'
            voting_model_file = 'voting_model.sav'

            ada_model = pickle.load(open(models_root + ada_model_file, 'rb'))
            forest_model = pickle.load(open(models_root + forest_model_file, 'rb'))
            forest_model_est_25 = pickle.load(open(models_root + forest_model_est_25_file, 'rb'))
            svm_model = pickle.load(open(models_root + svm_model_file, 'rb'))
            bagging_model = pickle.load(open(models_root + bagging_model_file, 'rb'))
            extra_tree_model = pickle.load(open(models_root + extra_tree_model_file, 'rb'))
            voting_model = pickle.load(open(models_root + voting_model_file, 'rb'))

            ada_result = ada_model.predict([parsed_hand_move])
            forest_result = forest_model.predict([parsed_hand_move])
            forest_est_25_result = forest_model_est_25.predict([parsed_hand_move])
            svm_model_result = svm_model.predict([parsed_hand_move])
            bagging_model_result = bagging_model.predict([parsed_hand_move])
            extra_tree_model_result = extra_tree_model.predict([parsed_hand_move])
            voting_model_result = voting_model.predict([parsed_hand_move])
            # 1 stone, 2 scisors, 3 paper
            print("------------------------------------------")
            print("1 stone, 2 scisors, 3 paper")
            print("ADA", ada_result[0])
            print("FOREST", forest_result[0])
            print("FOREST_EST_25", forest_est_25_result[0])
            print("SVM", svm_model_result[0])
            print("BAGGING", bagging_model_result[0])
            print("EXTRA TREE", extra_tree_model_result[0])
            print("VOTING", voting_model_result[0])

