from Evaluate import *
from DataModeling.DataModels import Span


def evaluate_attributes(patients):
    """Evaluate value, the span of the value, and the spans of all highlighted regions for each attribute"""
    for attribute_type in ALL_ATTRIBS:
        value_eval_data = EvaluationData()
        value_span_eval_data = EvaluationData()
        all_span_eval_data = EvaluationData()

        for patient in patients:
            for doc in patient.doc_list:
                evaluate_doc_attribute(attribute_type, doc,
                                       value_eval_data, value_span_eval_data, all_span_eval_data)


def evaluate_doc_attribute(attribute_type, doc, value_eval_data, value_span_eval_data, all_span_eval_data):
    """ For a specific attribute, find the correctness of selected value of attribute """
    gold_values, gold_value_spans, gold_all_spans = get_gold_field_data(attribute_type, doc)
    pred_values, pred_value_spans, pred_all_spans = get_predicted_field_data(attribute_type, doc)

    evaluate_value(value_eval_data, gold_values, pred_values)
    evaluate_value_span(value_span_eval_data, gold_value_spans, pred_value_spans)
    evaluate_all_spans(all_span_eval_data, gold_all_spans, pred_all_spans)


def get_gold_field_data(attribute_type, doc):
    """ For a field, find the gold field value, the span of the value, and the spans of all highlighted regions """
    value = {subst: None for subst in SUBSTANCE_TYPES}       # {subst: value}
    value_span = {subst: None for subst in SUBSTANCE_TYPES}  # {subst: span}
    all_spans = {subst: [] for subst in SUBSTANCE_TYPES}     # {subst: [all_spans]}

    for event in doc.gold_events:
        event_attribute_data(event, attribute_type, value, value_span, all_spans)

    return value, value_span, all_spans


def get_predicted_field_data(attribute_type, doc):
    """ For a field, find the gold field value, the span of the value, and the spans of all highlighted regions """
    value = {subst: None for subst in SUBSTANCE_TYPES}       # {subst: value}
    value_span = {subst: None for subst in SUBSTANCE_TYPES}  # {subst: span}
    all_spans = {subst: [] for subst in SUBSTANCE_TYPES}     # {subst: [all_spans]}

    for event in doc.predicated_events:
        event_attribute_data(event, attribute_type, value, value_span, all_spans)

    return value, value_span, all_spans


def event_attribute_data(event, attribute_type, value, value_span, all_spans):
    substance = event.substance_type
    attrib = event.attributes[attribute_type]

    value[substance] = attrib.text
    value_span[substance] = Span(attrib.span_start, attrib.span_end)
    all_spans[substance] = attrib.spans


def evaluate_value(value_eval_data, gold_values, pred_values):
    pass


def evaluate_value_span(value_span_eval_data, gold_value_spans, pred_value_spans):
    pass


def evaluate_all_spans(all_span_eval_data, gold_all_spans, pred_all_spans):
    pass
