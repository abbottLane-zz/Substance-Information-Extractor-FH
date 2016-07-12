import re
import string
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import cPickle as pickle

from SystemUtilities.Globals import *
from SystemUtilities.Configuration import *
from DataModeling.DataModels import Event


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
        pickle.dump(feature_map, open(featmap_file, "wb"))


def sentence_features_and_labels(patients):
    sent_feat_dicts = []    # List of sentence feature dictionaries
    labels_per_subst = {}       # Substance type : list of labels for each sentence (HAS/DOESN'T HAVE)

    for substance_type in SUBSTANCE_TYPES:
        labels_per_subst[substance_type] = []

    # grab sentence features and labels
    for patient in patients:
        for doc in patient.doc_list:
            for sent in doc.sent_list:
                # Features per sentence
                sent_features = get_features(sent)
                sent_feat_dicts.append(sent_features)

                # Labels per sentences
                for substance_type in SUBSTANCE_TYPES:
                    has_event = False
                    for gold_event in sent.gold_events:
                        if substance_type == gold_event.event_type:
                            has_event = True

                    if has_event:
                        labels_per_subst[substance_type].append(HAS_SUBSTANCE)
                    else:
                        labels_per_subst[substance_type].append(NO_SUBSTANCE)

    return sent_feat_dicts, labels_per_subst


def get_features(sent_obj):
    feats = {}

    grams = tokenize(sent_obj.text)

    # Unigrams
    for gram in grams:
        feats[gram] = True

    return feats


def tokenize(sent_text):
    sentence = sent_text.lower()
    grams = sentence.split()
    processed_grams = []

    left_omitted_chars = "|".join(["\$", "\."])
    right_omitted_chars = "|".join(["%"])
    ending_punc = re.sub(right_omitted_chars, "", string.punctuation)
    starting_punc = re.sub(left_omitted_chars, "", string.punctuation)

    for gram in grams:
        # Remove punctuation
        gram = gram.rstrip(ending_punc)
        gram = gram.lstrip(starting_punc)

        if gram:
            # Compress into word classes
            if gram.isdigit():
                processed_grams.append(NUMBER)
            elif re.sub("\.", "", gram).isdigit():
                processed_grams.append(DECIMAL)
            elif gram[0] == '$':
                processed_grams.append(MONEY)
            elif gram[len(gram) - 1] == '%':
                processed_grams.append(PERCENT)
            else:
                processed_grams.append(gram)

    return processed_grams


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


#################################
# Classification  ###############
#################################


# Add sentence-level predicted events in Patient object
def detect_sentence_events(patients):
    # Substances detected with ML classifier
    for substance_type in ML_CLASSIFIER_SUBSTANCES:
        classf, featmap = load_classifier(substance_type)

        for patient in patients:
            for doc in patient.doc_list:
                for sent in doc.sent_list:
                    classify_sent_for_substance(classf, featmap, sent, substance_type)

    # Substances detected with rules
    # TODO -- rule-based event detection for Drugs, Alc?


def load_classifier(event_type):
    classf_file = MODEL_DIR + event_type + EVENT_DETECT_MODEL_SUFFIX
    featmap_file = MODEL_DIR + event_type + EVENT_DETECT_FEATMAP_SUFFIX

    classifier = joblib.load(classf_file)
    feature_map = pickle.load(open(featmap_file, "rb"))

    return classifier, feature_map


def classify_sent_for_substance(classifier, featmap, sent, substance):
    sent_feats = get_features(sent)

    number_of_sentences = 1
    number_of_features = len(featmap)

    # Vectorize sentences and classify
    test_vectors = [vectorize_sentence(feats, featmap) for feats in sent_feats]
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
