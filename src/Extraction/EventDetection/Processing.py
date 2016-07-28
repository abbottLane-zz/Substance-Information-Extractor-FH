import re
import string
from SystemUtilities.Globals import *


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
                    has_event = check_sent_highlight_overlap(substance_type, sent, doc.highlighted_spans)

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


def check_sent_highlight_overlap(substance_type, sent, highlighted_spans):
    sent_has_subst = False

    for gold_span in highlighted_spans[substance_type]:
        # If sentence span is not completely before or after gold span, there must be overlap
        if not(sent.span_in_doc_end <= gold_span.start or sent.span_in_doc_start >= gold_span.stop):
            sent_has_subst = True

    return sent_has_subst
