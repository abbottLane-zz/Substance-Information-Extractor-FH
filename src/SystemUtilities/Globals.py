# User-specific configuration
will = "will"
spencer = "spencer"


# Runtime environments
class RUNTIME_ENV:
    TRAIN = "train"
    EXECUTE = "execute"


# Data Loading
BLOB_FIELDS = 5
METADATA_ROWS = 262882
CAISIS_ROWS = 2058
DELIMITER = r"1234567890qwertyuiop"

# Substances
SUBSTANCE = "SUBSTANCE"
ALCOHOL = "Alcohol"
DRUG = "Drug"
TOBACCO = "Tobacco"
SECONDHAND = "Secondhand"
SUBSTANCE_TYPES = [ALCOHOL, TOBACCO, SECONDHAND]
ML_CLASSIFIER_SUBSTANCES = [TOBACCO, ALCOHOL, SECONDHAND]  # Substances using ML classification for event detection
KEYWORD_SUBSTANCES = [TOBACCO, ALCOHOL]

# Classification Labels
HAS_SUBSTANCE = "has_subs_info"
NO_SUBSTANCE = "no_subs_info"

# Word/Gram Classes
NUMBER = "NUMBER"
DECIMAL = "DECIMAL"
MONEY = "MONEY"
PERCENT = "PERCENT"

# Statuses
STATUS = "STATUS"
UNKNOWN = "UNKNOWN"
CURRENT = "CURRENT"
FORMER = "FORMER"
YES = "YES"
NONE = "NONE"
STATUSES = [UNKNOWN, CURRENT, FORMER, YES, NONE]

# Attributes
TYPE = "TYPE"
AMOUNT = "AMOUNT"
DURATION = "DURATION"
QUIT_DATE = "QUITDATE"
QUIT_TIME_AGO = "QUITTIMEAGO"
QUIT_AGE = "QUITAGE"

ATTRIBS = dict()
ATTRIBS[TOBACCO] = [TYPE, AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]
ATTRIBS[SECONDHAND] = [AMOUNT]
ATTRIBS[ALCOHOL] = [AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]

# Model filename suffixes
EVENT_DETECT_MODEL_SUFFIX = "_detection_model.p"
STATUS_CLASSF_MODEL_SUFFIX = "_status_clsf_model.p"

EVENT_DETECT_FEATMAP_SUFFIX = "_detection_featmap.p"
STATUS_CLASSF_FEATMAP_SUFFIX = "_status_clsf_featmap.p"

# Substance Keyword/Regex files
KEYWORD_FILE_DIR = "..\Extraction\KeywordSearch\\"
KEYWORD_FILE_SUFFIX = "_Keywords.rgx"

# Keyword Hit Information
KEYWORD_HIT_NAME = "KeywordHit"
KEYWORD_HIT_TABLE = "Keywords"
POSITIVE = "Positive"
NEGATIVE = "Negative"
TOB_KEYWORD_VERSION = "TobaccoKeywordHit1.0"
ALC_KEYWORD_VERSION = "AlcoholKeywordHit1.0"
