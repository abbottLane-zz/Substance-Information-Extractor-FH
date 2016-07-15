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
    feature_map = Pickle.load(open(featmap_file, "rb"))

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


def evaluate(patients):
    fn_sents = {}   # {event type : [sentences]}
    fp_sents = {}   # {event type : [sentences]}
    tp = 0
    fn = 0
    fp = 0

    for event_type in ML_CLASSIFIER_SUBSTANCES:
        fn_sents[event_type] = []
        fp_sents[event_type] = []

    # Evaluate each sentence
    for doc in patients.doc_list:
        for sent in doc.sent_list:
            tp, fp, fn = evaluate_sentence(sent, fn_sents, fp_sents, tp, fp, fn)

    precision = float(tp) / float(tp + fp)
    recall = float(tp) / float(tp + fn)

    output_evaluation(precision, recall, fp_sents, fn_sents)


def evaluate_sentence(sentence, fn_sents, fp_sents, tp, fp, fn):
    gold_classfs = [e.type for e in sentence.gold_events]
    predicted_classfs = [p.type for p in sentence.predicted_events]

    # Find true pos, false pos, and false neg
    for classf in predicted_classfs:
        if classf in gold_classfs:
            tp += 1
        else:
            fp += 1
            fp_sents[classf].append(sentence.text)
    for classf in gold_classfs:
        if classf not in predicted_classfs:
            fn += 1
            fn_sents[classf].append(sentence.text)

    return tp, fp, fn


def output_evaluation(precision, recall, fp_sents, fn_sents):
    out_file = open(CLASSF_EVAL_FILENAME, "w")

    # Precision/recall
    out_file.write("\nClassifier Evaluation " + "\n---------------------\n")
    out_file.write("Precision: " + str(precision) + "\n")
    out_file.write("Recall: " + str(recall) + "\n\n")

    # Misclassified sentences
    out_file.write("<< FP Sentences >>\n")
    for event_type in fp_sents:
        out_file.write(event_type + "\n")
        for sent in fp_sents[event_type]:
            out_file.write(sent + "\n")

    out_file.write("<< FN Sentences >>\n")
    for event_type in fn_sents:
        out_file.write(event_type + "\n")
        for sent in fn_sents[event_type]:
            out_file.write(sent + "\n")
