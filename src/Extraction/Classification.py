import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC


def train_classifier(feature_dicts, labels):
    # Convert Data to vectors
    sent_vectors, labels_for_classifier, feature_map = vectorize_train_data(feature_dicts, labels)

    # Create Model
    classifier = LinearSVC()
    classifier.fit(sent_vectors, labels_for_classifier)

    return classifier, feature_map


def vectorize_train_data(sentences, labels):
    # convert to vectors
    dict_vec = DictVectorizer()
    sentence_vectors = dict_vec.fit_transform(sentences).toarray()

    # map features to the appropriate index in the established SVM vector representation for each classifier
    feature_names = dict_vec.get_feature_names()
    feature_map = {}
    for index, feat in enumerate(feature_names):
        feature_map[feat] = index

    return sentence_vectors, np.array(labels), feature_map
