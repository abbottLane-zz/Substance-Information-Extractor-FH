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


def classify_instance(classifier, feature_map, features):
    number_of_sentences = 1
    number_of_features = len(feature_map)

    # Vectorize sentences and classify
    test_vectors = [vectorize_sentence(feats, feature_map) for feats in features]
    test_array = np.reshape(test_vectors, (number_of_sentences, number_of_features))
    classifications = classifier.predict(test_array)

    return classifications


def vectorize_sentence(feats, feature_map):
    vector = [0 for _ in range(len(feature_map))]
    grams = feats.keys()
    for gram in grams:
        if gram in feature_map:
            index = feature_map[gram]
            vector[index] = 1
    return vector
