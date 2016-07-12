import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import cPickle as Pickle

from SystemUtilities.Configuration import *
from Processing import *


def train_event_detectors(patients):

    # Retrieve features and labels per every sentence
    sent_feat_dicts, labels_per_subst = sentence_features_and_labels(patients)

    for substance_type in ML_CLASSIFIER_SUBSTANCES:
        # Train classifier
        classifier, feature_map = train_detector(sent_feat_dicts, labels_per_subst[substance_type])

        # Save to file
        classf_file = MODEL_DIR + substance_type + EVENT_DETECT_MODEL_SUFFIX
        featmap_file = MODEL_DIR + substance_type + EVENT_DETECT_FEATMAP_SUFFIX

        joblib.dump(classifier, classf_file)
        Pickle.dump(feature_map, open(featmap_file, "wb"))


def train_detector(processed_sents, labels):
    # Convert Data to vectors
    sent_vectors, labels_for_classifier, feature_map = vectorize_train_data(processed_sents, labels)

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
