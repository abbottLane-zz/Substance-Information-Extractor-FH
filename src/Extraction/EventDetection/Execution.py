import numpy as np
from sklearn.externals import joblib
import cPickle as Pickle

from SystemUtilities.Configuration import *
from DataModeling.DataModels import Event
from Processing import *
from Extraction import Classification


# Add sentence-level predicted events in Patient object
def detect_sentence_events(patients):
    # Substances detected with ML classifier
    for substance_type in ML_CLASSIFIER_SUBSTANCES:
        classifier, feature_map = load_event_classifier(substance_type)

        for patient in patients:
            for doc in patient.doc_list:
                for sent in doc.sent_list:
                    classify_sent_for_substance(classifier, feature_map, sent, substance_type)

    # Substances detected with rules
    # -- would go here --


def load_event_classifier(event_type):
    classifier_file = MODEL_DIR + event_type + EVENT_DETECT_MODEL_SUFFIX
    feature_map_file = MODEL_DIR + event_type + EVENT_DETECT_FEATMAP_SUFFIX

    classifier, feature_map = Classification.load_classifier(classifier_file, feature_map_file)
    return classifier, feature_map


def classify_sent_for_substance(classifier, feature_map, sent, substance):
    sent_feats = get_features(sent)

    classifications = Classification.classify_instance(classifier, feature_map, sent_feats)

    # Add detected event to sentence
    if classifications[0] == HAS_SUBSTANCE:
        event = Event(substance)
        sent.predicted_events.append(event)



