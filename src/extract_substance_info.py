# extract and output substance information using the models trained in train_models.py
# output evaluation on test data or output results on unlabeled data

from SystemUtilities.Configuration import *
from DataModeling.DataModels import *
from Extraction.EventDetection import Execution as EventDetectExecution
from Extraction import Evaluation
from Extraction.AttributeExtraction import Execution as AttributeExtractionExec
from Extraction import PatientFromDocs, DocFromSents
from Extraction.StatusClassification import Execution
import DataLoading.DataLoader
from SystemUtilities import Shelver


def main():
    # Load Data
    patients = DataLoading.DataLoader.main(ENV)

    Shelver.shelve_patients(patients)
    # patients = Shelver.unshelve_patients()

    # Determine sentence level info
    extract_sentence_level_info(patients)

    # Determine document level info
    DocFromSents.get_doc_level_info(patients)

    # Determine patient level info
    PatientFromDocs.get_patient_level_info(patients)

    Shelver.shelve_full_patients(patients)
    # patients = Shelver.unshelve_full_patients()

    if ENV != RUNTIME_ENV.EXECUTE:
        evaluate_extraction(patients)

    return patients


def extract_sentence_level_info(patients):
    # Find substance references
    print("Classifying substance references...")
    sentences_with_events = EventDetectExecution.detect_sentence_events(patients)

    # Classify substance status
    print("Classifying substance status...")
    Execution.classify_sentence_status(sentences_with_events)

    # Extract Attributes
    print("Extracting Attributes...")
    AttributeExtractionExec.extract(sentences_with_events, stanford_ner_path=STANFORD_NER_PATH)
    tmp = 0


def evaluate_extraction(patients):
    # Event detection & Status classification
    Evaluation.evaluate_status_detection_and_classification(patients)

    # Extraction of each attribute

    # Event-Attribute linking?

    # Template?


if __name__ == '__main__':
    patient_substance_info = main()
