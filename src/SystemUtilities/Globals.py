# User-specific configuration
will = "will"
spencer = "spencer"
emily = "emily"

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
STATUS = "Status"
UNKNOWN = "UNKNOWN"
CURRENT = "CURRENT"
FORMER = "FORMER"
YES = "YES"
NON = "NON"
STATUSES = [UNKNOWN, CURRENT, FORMER, YES, NON]
POSITIVE_STATUSES = {CURRENT, FORMER, YES}
STATUS_HIERARCHY = [CURRENT, FORMER, YES, NON, UNKNOWN]

# Attributes
TYPE = "Type"
AMOUNT = "Amount"
DURATION = "Duration"
QUIT_DATE = "QuitDate"
QUIT_TIME_AGO = "QuitTimeAgo"
QUIT_AGE = "QuitAge"

ATTRIBS = dict()
ATTRIBS[TOBACCO] = [TYPE, AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]
ATTRIBS[SECONDHAND] = [AMOUNT]
ATTRIBS[ALCOHOL] = [AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]
ALL_ATTRIBS = [TYPE, AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]
FIELDS = [STATUS, TYPE, AMOUNT, DURATION, QUIT_DATE, QUIT_TIME_AGO, QUIT_AGE]

# Model filename suffixes
EVENT_DETECT_MODEL_SUFFIX = "_detection_model.p"
STATUS_CLASSF_MODEL_SUFFIX = "_status_clsf_model.p"
EVENT_FILLER_MODEL_NAME = "event_filler_model.p"

EVENT_DETECT_FEATMAP_SUFFIX = "_detection_featmap.p"
STATUS_CLASSF_FEATMAP_SUFFIX = "_status_clsf_featmap.p"
EVENT_FILLER_FEATMAP_NAME = "event_filler_featmap.p"

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
