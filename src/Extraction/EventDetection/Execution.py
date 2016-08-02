import numpy as np
from sklearn.externals import joblib
import cPickle as Pickle

from SystemUtilities.Configuration import *
from DataModeling.DataModels import Event
from Processing import *


# Add sentence-level predicted events in Patient object
def detect_sentence_events(patients):
    # Substances detected with ML classifier
    for substance_type in ML_CLASSIFIER_SUBSTANCES:
        classifier, feature_map = load_classifier(substance_type)

        for patient in patients:
            for doc in patient.doc_list:
                for sent in doc.sent_list:
                    classify_sent_for_substance(classifier, feature_map, sent, substance_type)

    # Substances detected with rules
    # -- would go here --


def load_classifier(event_type):
    classifier_file = MODEL_DIR + event_type + EVENT_DETECT_MODEL_SUFFIX
    feature_map_file = MODEL_DIR + event_type + EVENT_DETECT_FEATMAP_SUFFIX

    classifier = joblib.load(classifier_file)
    feature_map = Pickle.load(open(feature_map_file, "rb"))

    return classifier, feature_map


def classify_sent_for_substance(classifier, feature_map, sent, substance):
    sent_feats = get_features(sent)

    number_of_sentences = 1
    number_of_features = len(feature_map)

    # Vectorize sentences and classify
    test_vectors = [vectorize_sentence(feats, feature_map) for feats in sent_feats]
    test_array = np.reshape(test_vectors, (number_of_sentences, number_of_features))
    classifications = classifier.predict(test_array)

    # Add detected event to sentence
    if classifications[0] == HAS_SUBSTANCE:
        event = Event(substance)
        sent.predicted_events.append(event)


def vectorize_sentence(feats, feature_map):
    vector = [0 for _ in range(len(feature_map))]
    grams = feats.keys()
    for gram in grams:
        if gram in feature_map:
            index = feature_map[gram]
            vector[index] = 1
    return vector
