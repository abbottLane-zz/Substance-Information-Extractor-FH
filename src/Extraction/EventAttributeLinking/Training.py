from sklearn.externals import joblib
import cPickle as Pickle
from SystemUtilities.Parameter_Configuration import SURR_WORDS_WINDOW
from SystemUtilities.Configuration import *
from Globals import *
from Extraction import Classification


def train_event_fillers(patients):
    # Train model
    features, labels = features_and_labels(patients)
    classifier, feature_map = Classification.train_classifier(features, labels)

    # Write models to file
    classf_file = MODEL_DIR + EVENT_FILLER_MODEL_NAME
    featmap_file = MODEL_DIR + EVENT_FILLER_FEATMAP_NAME

    joblib.dump(classifier, classf_file)
    Pickle.dump(feature_map, open(featmap_file, "wb"))


def features_and_labels(patients):
    feature_sets = []   # Most recent keyword substance type, closest following keyword, sentence unigrams
    labels = []         # Attributes are assigned to a substance type

    for patient in patients:
        for doc in patient.doc_list:
            previous_sent = None
            for sent in doc.sent_list:
                for gold_event in sent.gold_events:
                    for attrib in gold_event.attributes:
                        add_attribute_feats_and_label(sent, gold_event, attrib, previous_sent, feature_sets, labels)
                previous_sent = sent

    return feature_sets, labels


def add_attribute_feats_and_label(sent, gold_event, attrib, previous_sent, feature_sets, labels):
    attrib_features = get_attribute_features(attrib, sent, previous_sent)
    feature_sets.append(attrib_features)
    labels.append(gold_event.substance_type)


def get_attribute_features(attrib, sent, previous_sent):
    attrib_feature_dict = {}

    # All event types found in current sentence and previous sentence
    __add_events_in_sent(attrib_feature_dict, sent.gold_events)
    __add_events_in_previous_sent(attrib_feature_dict, previous_sent.gold_events)

    # Attribute type and unigrams
    __add_attrib_property_feats(attrib_feature_dict, attrib)

    # Closest keywords
    __add_closest_left_keyword(attrib_feature_dict, attrib, sent, previous_sent)
    __add_closest_right_keyword(attrib_feature_dict, attrib, sent)

    # Surrounding words
    __add_surrounding_words(attrib_feature_dict, sent, attrib)

    return attrib_feature_dict


def __add_events_in_sent(attrib_feature_dict, events):
    for event in events:
        if event.status:
            feat = CURRENT_SENT_EVENT_TYPE + event.substance_type
            attrib_feature_dict[feat] = True


def __add_events_in_previous_sent(attrib_feature_dict, events):
    for event in events:
        if event.status:
            feat = CURRENT_SENT_EVENT_TYPE + event.substance_type
            attrib_feature_dict[feat] = True


def __add_attrib_property_feats(attrib_feature_dict, attrib):
    # Attribute type
    feat = ATTRIB_TYPE + attrib.type
    attrib_feature_dict[feat] = True

    # Attribute unigrams
    grams = attrib.text.split()
    for gram in grams:
        feat = ATTRIB_GRAM + gram
        attrib_feature_dict[feat] = True


def __add_closest_left_keyword(attrib_feature_dict, attrib, sent, previous_sent):
    # Check current sentence
    substance = find_closest_left_keyword_in_sent(attrib, sent)

    # If none in current sentence, check previous sentence
    if not substance:
        substance = find_closest_left_keyword_in_sent(attrib, previous_sent)

    # Add the feature
    attrib_feature_dict[CLOSEST_LEFT_KEYWORD] = substance


def __add_closest_right_keyword(attrib_feature_dict, attrib, sent):
    substance = find_closest_right_keyword_in_sent(attrib, sent)
    attrib_feature_dict[CLOSEST_RIGHT_KEYWORD] = substance


def find_closest_left_keyword_in_sent(attrib, sent):
    closest_end_index = 0
    closest_substance = ""

    for substance in sent.keyword_hits:
        if sent.keyword_hits[substance]:
            for keyword in sent.keyword_hits:
                # If keyword is before attribute
                if keyword.span_end < attrib.span_start:
                    # If keyword is the closest seen thus far
                    if keyword.span_end > closest_end_index:
                        closest_end_index = keyword.span_end
                        closest_substance = substance

    return closest_substance


def find_closest_right_keyword_in_sent(attrib, sent):
    closest_start_index = len(sent.text)
    closest_substance = ""

    for substance in sent.keyword_hits:
        if sent.keyword_hits[substance]:
            for keyword in sent.keyword_hits:
                # If keyword is after attribute
                if keyword.span_start > attrib.span_end:
                    # If keyword is the closest seen thus far
                    if keyword.span_start < closest_start_index:
                        closest_start_index = keyword.span_end
                        closest_substance = substance

    return closest_substance


def __add_surrounding_words(attrib_feature_dict, sent, attrib):
    """ Add words surrounding the attribute """
    # Grab and tokenize surrounding words
    words_before_attrib = __tokenize(sent.text[:attrib.span_start])
    words_after_attrib = __tokenize(sent.text[attrib.span_end:])

    # Add unigrams within window
    __add_surrounding_unigrams(attrib_feature_dict, words_before_attrib, words_after_attrib)


def __tokenize(sentence):
    return [w.lower() for w in sentence.split()]


def __add_surrounding_unigrams(attrib_feature_dict, words_before_attrib, words_after_attrib):
    # Get the index of where the window starts
    window_start_index = len(words_before_attrib) - SURR_WORDS_WINDOW
    if window_start_index < 0:
        window_start_index = 0

    # Words before the attribute
    for word in words_before_attrib[window_start_index:]:
        feature = SURR_WORD + word
        attrib_feature_dict[feature] = True

    # words after the attribute
    for word in words_after_attrib[:SURR_WORDS_WINDOW]:
        feature = SURR_WORD + word
        attrib_feature_dict[feature] = True
