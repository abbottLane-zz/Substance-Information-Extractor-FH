from Evaluate import *
from SystemUtilities.Configuration import SENT_EVENT_DETECT_EVAL_FILENAME, DOC_EVENT_DETECT_EVAL_FILENAME


def evaluate_status_classification(patients):
    """ Evaluate sentence and document level status"""
    sentence_eval_data = {subst: EvaluationData() for subst in SUBSTANCE_TYPES}
    doc_eval_data = {subst: EvaluationData() for subst in SUBSTANCE_TYPES}
    # Find tp, fp, fn
    for patient in patients:
        for doc in patient.doc_list:
            # Evaluate each document
            evaluate_doc_status_classification(doc, doc_eval_data)

            # Evaluate each sentence
            for sent in doc.sent_list:
                evaluate_sentence_status_classification(sent, sentence_eval_data)

def evaluate_event_detection(patients):
    """ Evaluate sentence and document level substance status info detection """
    sentence_eval_data = {subst: EvaluationData() for subst in SUBSTANCE_TYPES}
    doc_eval_data = {subst: EvaluationData() for subst in SUBSTANCE_TYPES}

    # Find tp, fp, fn
    for patient in patients:
        for doc in patient.doc_list:
            # Evaluate each document
            evaluate_doc_event_detection(doc, doc_eval_data)

            # Evaluate each sentence
            for sent in doc.sent_list:
                evaluate_sentence_event_detection(sent, sentence_eval_data)

    # Precision and recall
    calculate_and_output_eval(sentence_eval_data, doc_eval_data)


def calculate_and_output_eval(sentence_eval_data, doc_eval_data):
    for substance in SUBSTANCE_TYPES:
        # Calculate precision and recall
        sentence_eval_data[substance].calculate_precision_recall_f1()
        doc_eval_data[substance].calculate_precision_recall_f1()

        # Output evaluation
        sentence_filename = SENT_EVENT_DETECT_EVAL_FILENAME + "_" + substance
        doc_filename = DOC_EVENT_DETECT_EVAL_FILENAME + "_" + substance

        sentence_eval_data[substance].output(sentence_filename)
        doc_eval_data[substance].output(doc_filename)


def evaluate_sentence_status_classification(sent, sentence_eval_data):
    pass


def evaluate_sentence_event_detection(sent, sentence_eval_data):
    gold_substs = [g.substance_type for g in sent.gold_events]  # find_sent_gold_substs(sent, doc)
    predicted_substs = [p.substance_type for p in sent.predicted_events]

    compare_gold_and_predicted_substances(gold_substs, predicted_substs, sentence_eval_data, sent.text)


def evaluate_doc_status_classification(doc, doc_eval_data):
    gold_substs = {event.substance_type for event in doc.gold_events
                   if (event.status and event.status != UNKNOWN)}
    predicted_substs = {event.substance_type for event in doc.predicted_events}
    pass


def evaluate_doc_event_detection(doc, doc_eval_data):
    gold_substs = {event.substance_type for event in doc.gold_events
                   if (event.status and event.status != UNKNOWN)}
    predicted_substs = {event.substance_type for event in doc.predicted_events}

    compare_gold_and_predicted_status(gold_substs, predicted_substs, doc_eval_data, doc.id)

def compare_gold_and_predicted_status(gold_substs, predicted_substs, eval_data_per_substance, text):

    pass

def compare_gold_and_predicted_substances(gold_substs, predicted_substs, eval_data_per_substance, text):
    """ Record matches and mismatches for each substance """
    # Find true pos, false pos
    for classification in predicted_substs:
        if classification in gold_substs:
            eval_data_per_substance[classification].tp += 1
        else:
            eval_data_per_substance[classification].fp += 1
            eval_data_per_substance[classification].fp_values.append(text)
    # Find false neg
    for classification in gold_substs:
        if classification not in predicted_substs:
            eval_data_per_substance[classification].fn += 1
            eval_data_per_substance[classification].fn_values.append(text)


def find_sent_gold_substs(sent, doc):
    """@type doc: Document"""
    gold_substs = set()
    for substance in doc.highlighted_spans:
        for gold_span in doc.highlighted_spans[substance]:
            overlap = has_overlap(gold_span.start, gold_span.stop, sent.span_in_doc_start, sent.span_in_doc_end)
            if overlap:
                gold_substs.add(substance)
    return gold_substs
