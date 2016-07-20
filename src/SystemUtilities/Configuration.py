# Contains tunable system parameters

from SystemUtilities.Globals import *

# User-specific configuration
USER = spencer

# Environment/run type
ENV = RUNTIME_ENV.TRAIN

# User-specific paths
gold_annotation_dir = ""

if USER == spencer:
    data_dir = "C:\Users\sdmorris\Documents\FHCRC\ExposureProject\Substance_IE_Data\\"
    RAW_DATA_DIR = data_dir + r"exposure_notes.txt"
    METADATA_DIR = data_dir + r"metadata_for_clinic_notes.xlsx"
    CAISIS_DIR = data_dir + r"caisis_exposure_labels.xlsx"
    NOTE_OUTPUT_DIR = data_dir + r"SystemOutput\Notes\\"
    NOTE_OUTPUT_GOLD_LABELS_DIR = r"SystemOutput\Notes_annotations\\"
    MODEL_DIR = data_dir + r"SystemOutput\Models\\"

    ## GOLD annotation sources
    gold_annotation_dir = r"C:\Users\sdmorris\Documents\FHCRC\Resources\Florian\Florian_smoking\smoking_status\
                            SmokingStatusAnnotator\resources\gold\\"
    ## SILVER annotation sources
    silver_annotations_dir = "Silver annotations dir goes here"  # TODO: needs filled in
    ## Data sources
    data_repo_dir = r"C:\Users\sdmorris\Documents\FHCRC\Resources\Florian\Florian_smoking\smoking_status\sortedNotes\sortedNotes\\"

    # Output files
    CLASSF_EVAL_FILENAME = r"C:\Users\sdmorris\Documents\FHCRC\ExposureProject\Substance_IE_Data\SystemOutput\
                            Evaluation\EventDetectionEval.txt"
    SUBSTANCE_IE_DATA_FOLDER = r"C:\Users\sdmorris\Documents\FHCRC\ExposureProject\Substance_IE_Data\\"
    FLORIAN_FULL_DATA = "path/to/florian's/full/set/of/note/documents"

elif USER == will:
    RAW_DATA_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\exposure_notes_utf8.txt"
    METADATA_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\metadata_partdeux.xlsx"
    CAISIS_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\caisis_exposure_labels.xlsx"
    NOTE_OUTPUT_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\output\\"
    NOTE_OUTPUT_GOLD_LABELS_DIR = r"C:\Users\wlane\Documents\Substance_IE_Data\output_annotations\\"
    MODEL_DIR = "C:\Users\wlane\Documents\Substance_IE_Data\resources\Models\\"
    ## GOLD annotation sources
    gold_annotation_dir = r"C:\Users\wlane\Documents\Florian_smoking\smoking_status\SmokingStatusAnnotator\resources\gold\\"
    ## Silver Annotations sources
    silver_annotations_dir = r"C:\Users\wlane\Documents\Substance_IE_Data\resources\SilverOutput\\"
    ## Data sources
    data_repo_dir = r"C:\Users\wlane\Documents\Substance_IE_Data\output\\"
    # Output files
    CLASSF_EVAL_FILENAME = r"C:\Users\s____________________WILL'S PATH_____________________nce_IE_Data\SystemOutput\
                                Evaluation\EventDetectionEval.txt"
    SUBSTANCE_IE_DATA_FOLDER = r"C:\Users\wlane\Documents\Substance_IE_Data\\"
    FLORIAN_FULL_DATA = "C:\Users\wlane\Documents\Florian_smoking\smoking_status\\full_data_set\\"

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


# Set up which gold and raw data sets to use based on the ENV variable
def get_environment_gold_data(env):
    if env == RUNTIME_ENV.TRAIN:
        test_data = []
        train_data = [doc_train_gold_dir, patients_train_gold_dir]
        return test_data, train_data

    elif env == RUNTIME_ENV.TEST_DEV:
        test_data = [doc_dev_gold_dir, patients_dev_gold_dir]
        train_data = []
        return test_data, train_data

    elif env == RUNTIME_ENV.TEST_EVAL:
        test_data = [doc_test_gold_dir, patients_test_gold_dir]
        train_data = []
        return test_data, train_data

    elif env == RUNTIME_ENV.TRAIN_AND_TEST_DEV:
        test_data = [doc_dev_gold_dir, patients_dev_gold_dir]
        train_data = [patients_train_gold_dir, doc_train_gold_dir]
        return test_data, train_data

    elif env == RUNTIME_ENV.TRAIN_AND_TEST_EVAL:
        test_data = [doc_test_gold_dir, patients_test_gold_dir]
        train_data = [doc_train_gold_dir, patients_train_gold_dir]
        return test_data, train_data


def get_environment_text_data(env):
    return [data_repo_dir]
