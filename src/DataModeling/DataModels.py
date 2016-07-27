from SystemUtilities.Globals import *


# Source data data structures
class Data:
    def __init__(self, id_num):
        self.id = id_num
        self.gold_events = []
        self.predicted_events = []


class Patient(Data):
    def __init__(self, id_num):
        Data.__init__(self, id_num)
        self.doc_list = []


class Document(Data):
    def __init__(self, id_num, text):
        Data.__init__(self, id_num)
        self.text = text
        self.sent_list = []
        self.keyword_hits = {}  # {substance_type : [KeywordHit objs]}
        self.keyword_hits_json = {}

        for substance in SUBSTANCE_TYPES:
            self.keyword_hits[substance] = []


class Sentence(Data):
    def __init__(self, id_num, text):
        Data.__init__(self, id_num)
        self.text = text
        # self.span_in_doc_start = span_in_doc_start
        # self.span_in_doc_end = span_in_doc_end


# Substance information templates
class Event:
    def __init__(self, substance):
        self.substance = substance
        self.status = ""
        self.attributes = {}

        for attrib in ATTRIBS[substance]:
            self.attributes[attrib] = ""


class Attribute:
    def __init__(self, attribute_type, span_start, span_end, text):
        self.type = attribute_type
        self.span_start = span_start
        self.span_end = span_end
        self.text = text
