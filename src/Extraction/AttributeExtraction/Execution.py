import re
from nltk import StanfordNERTagger

from DataModeling.DataModels import Attribute
from SystemUtilities import Globals
from Extraction.AttributeExtraction.SentenceTokenizer import strip_sec_headers_tokenized_text
from SystemUtilities.Configuration import ATTRIB_EXTRACTION_DIR_HOME, STANFORD_NER_PATH
from SystemUtilities.Globals import entity_types


def extract(sentences_with_info, model_path=ATTRIB_EXTRACTION_DIR_HOME,
         stanford_ner_path=STANFORD_NER_PATH):

    # Divide sentence objects up by predicted abuse type
    sent_objs = get_sentences_containing_info_type(sentences_with_info)

    for type in entity_types: # {Amount, Duration, QuiteDate, TimeAgo, QuitAge, SecondhandAmount}
        for abuse_type in Globals.ML_CLASSIFIER_SUBSTANCES:
            curr_sentences = sent_objs[abuse_type]
            for sentobj in curr_sentences:
                model_name = model_path + "Models/" + "model-" + type + ".ser.gz"
                sentobj = test_model_in_mem(stanford_ner_path, model_name, sentobj, type, abuse_type)
    print("Finished CRF classification")

def get_sentences_containing_info_type(sentences_with_info):
    #Initialize dictionary
    sentences_by_abuse_type = dict()
    for subs_type in Globals.ML_CLASSIFIER_SUBSTANCES:
        sentences_by_abuse_type[subs_type] = list()

    for sent in sentences_with_info:
        for event in sent.predicted_events:
            sentences_by_abuse_type[event.substance_type].append(sent)
    return sentences_by_abuse_type



def test_model_in_mem(stanford_ner_path, model_name, sent_obj, type, abuse_type):
    stanford_tagger = StanfordNERTagger(
        model_name,
        stanford_ner_path,
        encoding='utf-8')

    text = sent_obj.text
    tokenized_text = list()
    spans = list()

    #Recover spans here
    for match in re.finditer("\S+", text):
        start = match.start()
        end = match.end()
        word = match.group(0)
        tokenized_text.append(word.rstrip(",.;:"))
        spans.append((start,end))
    tokenized_text = strip_sec_headers_tokenized_text(tokenized_text)
    classified_text = stanford_tagger.tag(tokenized_text)

    # Expand tuple to have span as well
    len_diff = len(spans) - len(classified_text) #Headers were stripped, so if this occured in the previous step, we have t account for the offset
    final_class_and_span = list()
    for idx,tup in enumerate(classified_text):
        combined = (classified_text[idx][0],classified_text[idx][1],spans[idx+len_diff][0],spans[idx+len_diff][1])
        final_class_and_span.append(combined)

    #print(classified_text)
    for event in sent_obj.predicted_events:
        if event.substance_type == abuse_type:
            attrib_list = get_attributes(final_class_and_span)
            if len(attrib_list) > 0:
                if type not in event.attributes:
                    event.attributes[type] = list()
                event.attributes[type] = attrib_list
    return sent_obj


def get_attributes(crf_classification_tuple_list):
    attribs = list()
    i = 0
    while i < len(crf_classification_tuple_list)-1:
        crf_classification_tuple = crf_classification_tuple_list[i]
        classL = crf_classification_tuple[1]
        start = crf_classification_tuple[2]
        if classL != "0": # beginning of a labeled span
            full_begin_span = start
            full_end_span = start
            full_text = ""
            while i < len(crf_classification_tuple_list)-1 and classL == crf_classification_tuple_list[i][1]:
                crf_classification_tuple = crf_classification_tuple_list[i]
                full_text += crf_classification_tuple[0] + " "
                full_end_span = crf_classification_tuple[3]
                i += 1
            attrib = Attribute(classL, full_begin_span, full_end_span, full_text)
            attribs.append(attrib)
        i += 1
    return attribs