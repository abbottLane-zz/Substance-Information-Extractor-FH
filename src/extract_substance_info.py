# extract and output substance information using the models trained in train_models.py
# output evaluation on test data or output results on unlabeled data

from SystemUtilities.Globals import *
from SystemUtilities.Configuration import *
from DataModeling.DataModels import *
from Extraction.EventDetection import Execution as EventDetect
import DataLoading.DataLoader


def main():
    # Load Data
    patients = DataLoading.DataLoader.main(ENV)

    # Determine sentence level info
    extract_sentence_level_info(patients)

    # Determine document level info

    # Determine patient level info

    if ENV != RUNTIME_ENV.EXECUTE:
        evaluate_extraction(patients)


def extract_sentence_level_info(patients):
    # Find substance references
    EventDetect.detect_sentence_events(patients)

    # Classify substance status

    # Find attributes

    # Tie attributes to substance references


def evaluate_extraction(patients):
    # Evaluate classification
    evaluate_sentence_level_info(patients)

    # Evaluate sentence level status & attributes

    # Evaluate document level status

    # Evaluate patient level status

    # Evaluate templates


def evaluate_sentence_level_info(patients):
    # Find substance references
    EventDetect.evaluate(patients)

    # Classify substance status

    # Find attributes

    # Tie attributes to substance references


if __name__ == '__main__':
    main()
