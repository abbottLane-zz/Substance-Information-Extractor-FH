# User-specific configuration
will = "will"
spencer = "spencer"

# Runtime environments
class RUNTIME_ENV:
    TRAIN = "train"
    TEST_DEV = "devtest"
    TEST_EVAL = "evaltest"
    TRAIN_AND_TEST_EVAL = "eval_train_test"
    TRAIN_AND_TEST_DEV = "test_train_test"
    EXECUTE = "execute"


# Data Loading
BLOB_FIELDS = 5
METADATA_ROWS = 262882
CAISIS_ROWS=2058
DELIMITER = r"1234567890qwertyuiop"

# Substances
SUBSTANCE = "SUBSTANCE"
ALCOHOL = "Alcohol"
DRUGS = "Drug"
TOBACCO = "Tobacco"
SUBSTANCE_TYPES = [ALCOHOL, DRUGS, TOBACCO]
ML_CLASSIFIER_SUBSTANCES = [TOBACCO]  # Substances using ML classification for event detection

# Classification Labels
HAS_SUBSTANCE = "has_subs_info"
NO_SUBSTANCE = "no_subs_info"

# Word/Gram Classes
NUMBER = "NUMBER"
DECIMAL = "DECIMAL"
MONEY = "MONEY"
PERCENT = "PERCENT"

# Statuses
UNKNOWN = "UNKNOWN"
CURRENT = "CURRENT"
FORMER = "FORMER"
YES = "YES"
NONE = "NONE"
STATUSES = [UNKNOWN, CURRENT, FORMER, YES, NONE]

# Model filename suffixes
EVENT_DETECT_MODEL_SUFFIX = "_detection_model.p"
STATUS_CLASSF_MODEL_SUFFIX = "_status_clsf_model.p"

EVENT_DETECT_FEATMAP_SUFFIX = "_detection_featmap.p"
STATUS_CLASSF_FEATMAP_SUFFIX = "_status_clsf_featmap.p"

# Substance Keyword/Regex files
KEYWORD_FILE_DIR = "..\Extraction\KeywordSearch\\"
KEYWORD_FILE_SUFFIX = "_Keywords.txt"

# Keyword Hit Information
KEYWORD_HIT_NAME = "KeywordHit"
KEYWORD_HIT_TABLE = "Keywords"
POSITIVE = "Positive"
NEGATIVE = "Negative"
TOB_KEYWORD_VERSION = "TobaccoKeywordHit1.0"
ALC_KEYWORD_VERSION = "AlcoholKeywordHit1.0"
