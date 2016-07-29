# Contains tunable system parameters

from SystemUtilities.Globals import *

# User-specific configuration
USER = will

# Environment/run type
ENV = RUNTIME_ENV.TRAIN

# User-specific paths
gold_annotation_dir = ""

if USER == spencer:
    data_dir = "C:\Users\sdmorris\Documents\FHCRC\ExposureProject\Substance_IE_Data\\"
    florian_dir = r"C:\Users\sdmorris\Documents\FHCRC\Resources\Florian\Florian_smoking\smoking_status\\"
    RAW_DATA_DIR = data_dir + r"exposure_notes.txt"
    METADATA_DIR = data_dir + r"metadata_for_clinic_notes.xlsx"
    CAISIS_DIR = data_dir + r"caisis_exposure_labels.xlsx"
    NOTE_OUTPUT_DIR = data_dir + r"SystemOutput\Notes\\"
    TRAIN_SPLIT_DIR = data_dir + r"notes_training\\"
    DEV_SPLIT_DIR = data_dir + r"notes_dev\\"
    TEST_SPLIT_DIR = data_dir + r"notes_testing\\"
    NOTE_OUTPUT_GOLD_LABELS_DIR = r"SystemOutput\Notes_annotations\\"
    MODEL_DIR = data_dir + r"SystemOutput\Models\\"
    # GOLD annotation sources
    gold_annotation_dir = florian_dir + r"SmokingStatusAnnotator\resources\gold\\"
    # Data sources
    data_repo_dir = florian_dir + r"sortedNotes\sortedNotes\combined\\"
    dev_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_dev.csv"
    test_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_test.csv"
    train_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_train.csv"
    # Output files
    CLASSF_EVAL_FILENAME = data_dir + r"SystemOutput\Evaluation\EventDetectionEval.txt"
    SUBSTANCE_IE_DATA_FOLDER = data_dir
    FLORIAN_FULL_DATA = florian_dir + r"sortedNotes\sortedNotes\combined\\"
    METADATA_OUT = data_dir + r"SystemOutput\Metadata"
    DOCS_NEEDING_ANNOTATION_DIR = data_dir + r"SystemOutput\DocsToAnnotate\\"
elif USER == will:
    RAW_DATA_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\exposure_notes_utf8.txt"
    METADATA_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\metadata_partdeux.xlsx"
    CAISIS_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\caisis_exposure_labels.xlsx"
    NOTE_OUTPUT_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\output\\"
    TRAIN_SPLIT_DIR =  r"C:\Users\wlane\Documents\Substance_IE_Data\notes_training\\"
    DEV_SPLIT_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\notes_dev"
    TEST_SPLIT_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\notes_testing\\"
    NOTE_OUTPUT_GOLD_LABELS_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\output_annotations\\"
    MODEL_DIR = "C:\Users\wlane\Documents\Substance_IE_Data\resources\Models\\"
    ## GOLD annotation sources
    gold_annotation_dir = r"C:\Users\wlane\Documents\Florian_smoking\smoking_status\SmokingStatusAnnotator\resources\gold\\"

    ## Data sources
    data_repo_dir = r"C:\Users\wlane\Documents\Substance_IE_Data\output\\"
    dev_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_dev.csv"
    test_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_test.csv"
    train_csv = "C:\Users\wlane\Documents\Substance_IE_Data\FLOR_filtered_tsv\\flor_train.csv"
    # Output files
    CLASSF_EVAL_FILENAME = r"C:\Users\s____________________WILL'S PATH_____________________nce_IE_Data\SystemOutput\
                                Evaluation\EventDetectionEval.txt"
    SUBSTANCE_IE_DATA_FOLDER = r"C:\Users\wlane\Documents\Substance_IE_Data\\"
    FLORIAN_FULL_DATA = "C:\Users\wlane\Documents\Florian_smoking\smoking_status\\full_data_set\\"
    DOCS_NEEDING_ANNOTATION_DIR =  r"C:\Users\wlane\Documents\Substance_IE_Data\Docs_to_annotate\\"


else:
    print("Error: unknown user in SystemUtilities/Configuration")

doc_all_gold_dir = gold_annotation_dir + "documents.GOLD"
doc_dev_gold_dir = gold_annotation_dir + "documents_dev.GOLD"
doc_test_gold_dir = gold_annotation_dir + "documents_testing.GOLD"
doc_train_gold_dir = gold_annotation_dir + "documents_training.GOLD"
patients_all_gold_dir = gold_annotation_dir + "patients.GOLD"
patients_dev_gold_dir = gold_annotation_dir + "patients_dev.GOLD"
patients_test_gold_dir = gold_annotation_dir + "patients_testing.GOLD"
patients_train_gold_dir = gold_annotation_dir + "patients_training.GOLD"
i2b2_test_gold_dir = gold_annotation_dir + "i2b2\i2b2_test.GOLD"
i2b2_train_gold_dir = gold_annotation_dir + "i2b2\i2b2_train.GOLD"
flor_sentence_level_annotations_dir = gold_annotation_dir + "\sentences"

