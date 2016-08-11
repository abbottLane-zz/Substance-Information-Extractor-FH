# extract and output substance information using the models trained in train_models.py
# output evaluation on test data or output results on unlabeled data

from SystemUtilities.Globals import *
from SystemUtilities.Configuration import *
from DataModeling.DataModels import *
from Extraction.EventDetection import Execution as EventDetect
from Extraction.EventAttributeLinking import Execution as EventFilling
from Extraction import PatientFromDocs, DocFromSents
from Extraction.StatusClassification import Execution
import DataLoading.DataLoader


def main():
    # Load Data
    patients = DataLoading.DataLoader.main(ENV)

    # Determine sentence level info
    extract_sentence_level_info(patients)

    # Determine document level info
    DocFromSents.get_doc_level_info(patients)

    # Determine patient level info
    PatientFromDocs.get_patient_level_info(patients)

    # TODO -- Do something with filled patients object

    if ENV != RUNTIME_ENV.EXECUTE:
        evaluate_extraction(patients)


def extract_sentence_level_info(patients):
    # Find substance references
    print("Classifying substance references...")
    sentences_with_events = EventDetect.detect_sentence_events(patients)

    # Classify substance status
    print("Classifying substance status...")
    Execution.classify_sentence_status(sentences_with_events)
    tmp = 0

    # Find attributes

    # Tie attributes to substance references
    EventFilling.link_attributes_to_substances(patients)


def evaluate_extraction(patients):
    # Sentence level
    evaluate_sent_level_info(patients)

    # Evaluate document level status
    evaluate_doc_level_info(patients)

    # Evaluate patient level status

    # Evaluate templates


def evaluate_sent_level_info(patients):
    # Status info detection and each attribute

    pass


def evaluate_doc_level_info(patients):
    # Event detection
    EventDetect.evaluate(patients)

    # Status classification

    # Extraction of each attribute

    # Event-Attribute linking

    # Template
    pass


def evaluate_patient_level_info(patients):
    # Status classification

    # Each attribute

    # Template
    pass


if __name__ == '__main__':
    main()
