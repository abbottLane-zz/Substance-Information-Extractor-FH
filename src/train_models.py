# train classifiers and extractors and output models

from Extraction.EventDetection import Training as EventDetectionTraining


def main():
    # Load Data
    patients = []  # list of filled Patient objects

    # Event Detection
    EventDetectionTraining.train_event_detectors(patients)

    # Status classification

    # Attribute Extraction

    # Event Filling

    pass


if __name__ == '__main__':
    main()
