import re

from SystemUtilities.Globals import *


class KeywordHitJSON:
    def __init__(self, substance):
        self.alg_version = ""
        self.init_version(substance)

        self.name = substance + KEYWORD_HIT_NAME
        self.confidence = 0
        self.spans = []
        self.table = KEYWORD_HIT_TABLE
        self.value = NEGATIVE

    def init_version(self, substance):
        if substance == TOBACCO:
            self.alg_version = TOB_KEYWORD_VERSION
        elif substance == ALCOHOL:
            self.alg_version = ALC_KEYWORD_VERSION


class KeywordHit:
    def __init__(self, text, span_start, span_end):
        self.text = text
        self.span_start = span_start
        self.span_end = span_end


class Span:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


def search_keywords(patients):
    docs_with_hits = set()
    for substance in SUBSTANCE_TYPES:
        regexes = get_regexes_from_file(substance)
        docs_with_substance = find_keyword_hits(patients, regexes, substance)

        for doc in docs_with_substance:
            docs_with_hits.add(doc)

    return docs_with_hits


def get_regexes_from_file(substance):
    filename = KEYWORD_FILE_DIR + substance + KEYWORD_FILE_SUFFIX
    with open(filename, "r") as regex_file:
        regex_lines = regex_file.readlines()
        regexes = [r[:-1] for r in regex_lines]     # remove "\n" at end of each regex line

    # OR regexes together to get one big regex
    regex = r"((" + ")|(".join(regexes) + "))"
    single_regex = [regex]
    return single_regex


def find_keyword_hits(patients, regexes, substance):
    docs_with_hits = []

    for patient in patients:
        for doc in patient.doc_list:
            keywordhit_json = KeywordHitJSON(substance)

            has_hit = False
            for regex in regexes:
                # JSON format hits
                find_json_doc_hits(doc, regex, keywordhit_json)

                # Debug format hits
                doc_hits = find_doc_hits(doc, regex)
                doc.keyword_hits[substance].extend(doc_hits)
                if doc_hits:
                    has_hit = True

            doc.keyword_hits_json[substance] = keywordhit_json
            if has_hit:
                docs_with_hits.append(doc)

    return docs_with_hits


def find_doc_hits(doc, regex):
    matches = re.finditer(regex, doc.text, re.IGNORECASE)
    hits = []
    for match in matches:
        keyword_text = match.group()
        span = match.span()

        span_start = span[0]
        span_end = span[1]

        hit = KeywordHit(keyword_text, span_start, span_end)
        hits.append(hit)
    return hits


def find_json_doc_hits(doc, regex, keywordhit_json):
    matches = re.finditer(regex, doc.text, re.IGNORECASE)

    for match in matches:
        span_tuple = match.span()
        span = Span(span_tuple[0], span_tuple[1])

        keywordhit_json.spans.append(span)
        keywordhit_json.value = POSITIVE
