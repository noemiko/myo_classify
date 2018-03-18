import sklearn.ensemble
from sklearn import metrics
from sklearn import svm
import pickle
from data_processing import process_from_files
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np


def learn():
    stone_training_set, paper_training_set, scisors_training_set = process_from_files()
    classes = create_matching_classes_list(stone_training_set, paper_training_set, scisors_training_set)
    model_ada_bost = sklearn.ensemble.AdaBoostClassifier(n_estimators=7, learning_rate=1)
    model_random_forest = sklearn.ensemble.RandomForestClassifier()
    model_random_forest_estimator_25 = sklearn.ensemble.RandomForestClassifier(n_estimators=25)
    model_svm = svm.SVC()
    model_bagging = sklearn.ensemble.BaggingClassifier()
    model_extra_tree = sklearn.ensemble.ExtraTreesClassifier()
    model_gausian = GaussianNB()
    model_neural_network = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 1), random_state=1)


    clf1 = LogisticRegression(random_state=123)
    clf2 = RandomForestClassifier(random_state=123)
    clf3 = GaussianNB()
    voting_model = sklearn.ensemble.VotingClassifier(
        estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)],
        voting='soft',
        weights=[1, 1, 5])


    all_training_set = stone_training_set[:15]+scisors_training_set[:15]+paper_training_set[:15]
    test_set = stone_training_set[-5:]+scisors_training_set[-5:]+paper_training_set[-5:]

    all_training_set = np.array(all_training_set).astype(np.int)
    test_set = np.array(test_set).astype(np.int)

    model_ada_bost.fit(all_training_set, classes)
    model_random_forest.fit(all_training_set, classes)
    model_random_forest_estimator_25.fit(all_training_set, classes)
    model_svm.fit(all_training_set, classes)
    model_bagging.fit(all_training_set, classes)
    model_extra_tree.fit(all_training_set, classes)
    voting_model.fit(all_training_set, classes)
    model_gausian.fit(all_training_set, classes)
    model_gausian.fit(all_training_set, classes)
    model_neural_network.fit(all_training_set, classes)

    ada_predict = model_ada_bost.predict(test_set)
    random_forest_1 = model_random_forest.predict(test_set)
    random_forest_2 = model_random_forest_estimator_25.predict(test_set)
    svm_predict = model_svm.predict(test_set)
    bagging_predict = model_bagging.predict(test_set)
    extra_tree_predict = model_extra_tree.predict(test_set)
    voting_predict = voting_model.predict(test_set)
    gausian_predict = model_gausian.predict(test_set)
    neural_predict = model_neural_network.predict(test_set)

    test_classes = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3]
    print('ADA : ', metrics.accuracy_score(test_classes, ada_predict))
    print('RANDOM1 : ', metrics.accuracy_score(test_classes, random_forest_1))
    print('RANDOM2 : ', metrics.accuracy_score(test_classes, random_forest_2))
    print('SVM : ', metrics.accuracy_score(test_classes, svm_predict))
    print('BAGING : ', metrics.accuracy_score(test_classes, bagging_predict))
    print('EXTRA TREE : ', metrics.accuracy_score(test_classes, extra_tree_predict))
    print('VOTING : ', metrics.accuracy_score(test_classes, voting_predict))
    print('GAUSIAN : ', metrics.accuracy_score(test_classes, gausian_predict))
    print('NEURAL : ', metrics.accuracy_score(test_classes, neural_predict))

    models_root = "models/"
    ada_model_file = 'ada_model.sav'
    forest_model_file = 'forest_model.sav'
    forest_model_est_25_file = 'forest_est_25_model.sav'
    svm_model_file = 'svm_model.sav'
    bagging_model_file = 'bagging_model.sav'
    extra_tree_model_file = 'extra_tree_model.sav'
    voting_model_file = 'voting_model.sav'

    pickle.dump(model_ada_bost, open(models_root+ada_model_file, 'wb'))
    pickle.dump(model_random_forest, open(models_root+forest_model_file, 'wb'))
    pickle.dump(model_random_forest_estimator_25, open(models_root+forest_model_est_25_file, 'wb'))
    pickle.dump(model_svm, open(models_root+svm_model_file, 'wb'))
    pickle.dump(model_svm, open(models_root+bagging_model_file, 'wb'))
    pickle.dump(model_svm, open(models_root+extra_tree_model_file, 'wb'))
    pickle.dump(model_svm, open(models_root+voting_model_file, 'wb'))


def create_matching_classes_list(stone_training_set, scisors_training_set, paper_training_set):
    classes_set = []
    classes_set += 15 * [1]
    classes_set += 15 * [2]
    classes_set += 15 * [3]
    return classes_set


if __name__ == "__main__":
    learn()
