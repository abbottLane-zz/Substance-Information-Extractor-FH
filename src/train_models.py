# train classifiers and extractors and output models
import DataLoading.DataLoader
from Extraction.EventDetection import Training as EventDetectionTraining
from Extraction.StatusClassification import Training as StatusClassificationTraining
from Extraction.EventAttributeLinking import Training as EventFillerTraining
from Extraction.AttributeExtraction import Training as AttributeExtractionTraining
from SystemUtilities import Shelver
from SystemUtilities.Configuration import ENV


def main():
    # Set ENV variable to TRAIN
    ENV = DataLoading.DataLoader.RUNTIME_ENV.TRAIN

    # Load Data
    patients = DataLoading.DataLoader.main(ENV)  # list of filled Patient objects

    Shelver.shelve_patients(patients)
    # patients = Shelver.unshelve_patients()

    # Event Detection
    EventDetectionTraining.train_event_detectors(patients)

    # Status classification
    StatusClassificationTraining.train_status_classifier(patients)

    # Attribute Extraction
    AttributeExtractionTraining.train(patients)

    # Event Filling
    EventFillerTraining.train_event_fillers(patients)


if __name__ == '__main__':
    main()
