from tools import get_accuracy
import datetime


def test_knn():
    """
    test the classifier based on KNN
    """
    print("KNNClassifier")
    print("---" * 45)

    from classifiers import KNNClassifier
    # k = [1, 3, 5, 7, 9, 11, 13]
    # k = [21, 25, 29, 33, 37, 41, 45]
    k = 3
    knn = KNNClassifier(train_data, train_labels, k=k, best_words=best_words)

    classify_labels = []

    print("KNNClassifiers is testing ...")
    for data in test_data:
        classify_labels.append(knn.classify(data))
    print("KNNClassifiers tests over.")

    filepath = "runout/KNN-movie-pt-%d-%d-nt-%d-%d-f-%d-k-%d-%s.xls" % (
        pos_train_num, pos_test_num, neg_train_num, neg_test_num, feature_num, k,
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    get_accuracy(test_labels, classify_labels, parameters, filepath)


def test_bayes():
    """
    test the classifier based on Naive Bayes
    """
    print("BayesClassifier")
    print("---" * 45)

    from classifiers import BayesClassifier
    bayes = BayesClassifier(train_data, train_labels, best_words)

    classify_labels = []
    print("BayesClassifier is testing ...")
    for data in test_data:
        classify_labels.append(bayes.classify(data))
    print("BayesClassifier tests over.")

    filepath = "runout/Bayes-movie-pt-%d-%d-nt-%d-%d-f-%d-%s.xls" % (
        pos_train_num, pos_test_num, neg_train_num, neg_test_num, feature_num,
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    get_accuracy(test_labels, classify_labels, parameters, filepath)


def test_maxent():
    """
    test the classifier based on Maximum Entropy
    """
    print("MaxEntClassifier")
    print("---" * 45)

    from classifiers import MaxEntClassifier
    maxent = MaxEntClassifier(train_data, train_labels, best_words, max_iter)

    classify_labels = []
    print("MaxEntClassifier is testing ...")
    for data in test_data:
        classify_labels.append(maxent.classify(data))
    print("MaxEntClassifier tests over.")

    filepath = "runout/MaxEnt-movie-pt-%d-%d-nt-%d-%d-f-%d-iter-%d-%s.xls" % (
        pos_train_num, pos_test_num, neg_train_num, neg_test_num, feature_num, max_iter,
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    get_accuracy(test_labels, classify_labels, parameters, filepath)


def test_svm():
    """
    test the classifier based on Support Vector Machine
    """
    print("SVMClassifier")
    print("---" * 45)

    from sklearn.svm import SVR
    import numpy as np

    def get(datas):
        vectors = []
        for data in datas:
            vector = []
            for feature in best_words:
                vector.append(data.count(feature))
            vectors.append(vector)
        return np.array(vectors)

    train_vectors = get(train_data)
    test_vectors = get(test_data)
    labels = np.array(train_labels)

    # svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # svr_rbf.fit(train_vectors, labels)
    # classify_labels = svr_rbf.predict(test_vectors)
    svr_lin = SVR(kernel='linear', C=1e3)
    svr_lin.fit(train_vectors, labels)
    classify_labels = svr_lin.predict(test_vectors)
    print(classify_labels)

    classify_labels = [1 if label > 0.1 else 0 for label in classify_labels]

    # svr_lin = SVR(kernel='linear', C=1e3)
    # svr_lin.fit(train_vectors, labels)
    # classify_labels = svr_lin.predict(test_vectors)
    # print(classify_labels)
    #
    # svr_rbf.fit(train_vectors, labels)
    # svr_poly.fit(train_vectors, labels)
    # classify_labels = svr_poly.predict(test_vectors)
    # print(classify_labels)
    #
    # from classifiers import SVMClassifier
    # svm = SVMClassifier(["".join(data) for data in train_data], train_labels)
    #
    # classify_labels = []
    # print("SVMClassifier is testing ...")
    # for data in test_data:
    #     classify_labels.append(svm.classify("".join(data)))
    # print("SVMClassifier tests over.")
    #
    filepath = "runout/SVM-movie-pt-%d-%d-nt-%d-%d-tfidf-%s-lin.xls" % (
        pos_train_num, pos_test_num, neg_train_num, neg_test_num,
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    get_accuracy(test_labels, classify_labels, parameters, filepath)


def test_multiple_classifiers():
    """
    test the Fusion of Multiple Classifiers
    """
    print("Fusion of Multiple Classifiers")
    print("---" * 45)

    from classifiers import MovieMultipleClassifiers

    # get the instance of classifiers
    prob = False
    # prob = True
    knn = False

    mc = MovieMultipleClassifiers(train_data, train_labels, best_words, max_iter, knn)

    print("movieMultipleClassifiers is testing ...")
    classify_labels = []
    for data in test_data:
        classify_labels.append(mc.classify(data, prob))

    print("movieMultipleClassifiers tests over.")

    filepath = "runout/Multiple-movie-pt-%d-%d-nt-%d-%d-iter-%d-k-%s-prob-%s-%s.xls" % (
        pos_train_num, pos_test_num, neg_train_num, neg_test_num, max_iter, "True" if knn else "False",
        "True" if prob else "False", datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    get_accuracy(test_labels, classify_labels, parameters, filepath)


if __name__ == "__main__":
    pos_train_num = neg_train_num = 500
    pos_test_num = neg_test_num = 200
    feature_num = 4000
    max_iter = 100
    parameters = [pos_train_num, neg_train_num, pos_test_num, neg_test_num, feature_num]

    # get the corpus_
    from corpus import MovieCorpus

    corpus = MovieCorpus()
    train_data, train_labels = corpus.get_train_corpus(pos_train_num, neg_train_num)
    test_data, test_labels = corpus.get_test_corpus(pos_test_num, neg_test_num)

    # feature extraction
    from feature_extraction import ChiSquare

    fe = ChiSquare(train_data, train_labels)
    best_words = fe.best_words(feature_num)

    # test knn
    # test_knn()

    # test bayes
    # test_bayes()

    # test maxent
    # test_maxent()

    # test SVM
    # test_svm()
    # SVM_sklearn()

    # test multiple_classifiers
    test_multiple_classifiers()



