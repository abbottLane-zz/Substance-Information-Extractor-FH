import re

from SystemUtilities.Globals import *


class KeywordHit:
    def __init__(self, text, span_start, span_end):
        self.text = text
        self.span_start = span_start
        self.span_end = span_end


def search_keywords(substance, patients):
    docs_with_hits = []
    if substance in SUBSTANCE_TYPES:
        regexes = get_regexes_from_file(substance)
        docs_with_hits = find_keyword_hits(patients, regexes, substance)
    else:
        print("Unexpected substance name")

    return docs_with_hits


def get_regexes_from_file(substance):
    filename = KEYWORD_FILE_DIR + substance + KEYWORD_FILE_SUFFIX
    with open(filename, "r") as regex_file:
        regex_lines = regex_file.readlines()
        regexes = [r[:-1] for r in regex_lines]     # remove "\n" at end of each regex line
    return regexes


def find_keyword_hits(patients, regexes, substance):
    docs_with_hits = []

    for patient in patients:
        for doc in patient.doc_list:

            has_hit = False
            for regex in regexes:
                doc_hits = find_doc_hits(doc, regex)
                doc.keyword_hits[substance].extend(doc_hits)
                if doc_hits:
                    has_hit = True

            if has_hit:
                docs_with_hits.append(doc)

    return docs_with_hits


def find_doc_hits(doc, regex):
    matches = re.finditer(regex, doc.text)
    hits = []
    for match in matches:
        keyword_text = match.group()
        span = match.span()

        span_start = span[0]
        span_end = span[1]

        hit = KeywordHit(keyword_text, span_start, span_end)
        hits.append(hit)
    return hits
