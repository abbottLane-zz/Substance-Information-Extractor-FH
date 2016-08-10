# train classifiers and extractors and output models
import DataLoading.DataLoader
from Extraction.EventDetection import Training as EventDetectionTraining
from Extraction.StatusClassification import Training as StatusClassificationTraining
from SystemUtilities.Configuration import ENV


def main():
    # Load Data
    patients = DataLoading.DataLoader.main(ENV)  # list of filled Patient objects

    # Event Detection
    EventDetectionTraining.train_event_detectors(patients)

    # Status classification
    StatusClassificationTraining.train_status_classifier(patients)

    # Attribute Extraction

    # Event Filling

    pass


if __name__ == '__main__':
    main()
