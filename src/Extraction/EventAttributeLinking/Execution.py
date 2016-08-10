from sklearn.externals import joblib
import cPickle as Pickle
from SystemUtilities.Configuration import *
import Processing
from Extraction import Classification


def link_attributes_to_substances(patients):
    classifier, feature_map = load_classifier()

    substance_attributes = find_attributes_per_substance(classifier, feature_map, patients)

    # Choose which attributes to keep
    # TODO

    # Put selected attributes in the document level
    # TODO


def load_classifier():
    classifier_file = MODEL_DIR + EVENT_FILLER_MODEL_NAME
    feature_map_file = MODEL_DIR + EVENT_FILLER_FEATMAP_NAME

    classifier = joblib.load(classifier_file)
    feature_map = Pickle.load(open(feature_map_file, "rb"))

    return classifier, feature_map


def find_attributes_per_substance(classifier, feature_map, patients):
    """ Get all attributes assigned to each substance -- {substance: field: [Attributes]} """
    attribs_found_per_substance = {subst: {field: [] for field in ATTRIBS[subst]} for subst in SUBSTANCE_TYPES}

    # Get features
    attrib_feature_sets, attributes = Processing.features(patients)

    # Get classifications
    for attrib, features in zip(attributes, attrib_feature_sets):
        classifications = Classification.classify_instance(classifier, feature_map, features)

        # Assign attribute to substance identified
        classified_substance = classifications[0]
        if classified_substance in SUBSTANCE_TYPES:
            attribs_found_per_substance[classified_substance].append(attrib)

    return attribs_found_per_substance
