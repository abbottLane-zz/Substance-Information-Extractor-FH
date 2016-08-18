from Evaluate import *
from SystemUtilities.Configuration import SENT_EVENT_DETECT_EVAL_FILENAME, DOC_EVENT_DETECT_EVAL_FILENAME


def evaluate_status_detection_and_classification(patients):
    """ Evaluate sentence and document level substance status info detection """
    sentence_eval_data = EvaluationData()
    doc_eval_data = EvaluationData()

    # Find tp, fp, fn
    for patient in patients:
        for doc in patient.doc_list:
            # Evaluate each document
            evaluate_doc_event_detection(doc, doc_eval_data)

            # Evaluate each sentence
            for sent in doc.sent_list:
                evaluate_sentence_event_detection(sent, sentence_eval_data)

    # Precision and recall
    sentence_eval_data.calculate_precision_recall_f1()
    doc_eval_data.calculate_precision_recall_f1()

    # Output evaluation
    sentence_eval_data.output(SENT_EVENT_DETECT_EVAL_FILENAME)
    doc_eval_data.output(DOC_EVENT_DETECT_EVAL_FILENAME)


def evaluate_sentence_event_detection(sent, sentence_eval_data):
    gold_substs = [g.substance_type for g in sent.gold_events]  # find_sent_gold_substs(sent, doc)
    predicted_substs = [p.substance_type for p in sent.predicted_events]

    compare_gold_and_predicted_substances(gold_substs, predicted_substs, sentence_eval_data, sent.text)


def evaluate_doc_event_detection(doc, doc_eval_data):
    gold_substs = {event.substance_type for event in doc.gold_events
                   if (event.substance_type and event.substance_type != UNKNOWN)}
    predicted_substs = {event.substance_type for event in doc.predicted_events}

    compare_gold_and_predicted_substances(gold_substs, predicted_substs, doc_eval_data, doc.id)


def compare_gold_and_predicted_substances(gold_substs, predicted_substs, eval_data, text):
    # Find true pos, false pos
    for classification in predicted_substs:
        if classification in gold_substs:
            eval_data.tp += 1
        else:
            eval_data.fp += 1
            eval_data.fp_sents[classification].append(text)
    # Find false neg
    for classification in gold_substs:
        if classification not in predicted_substs:
            eval_data.fn += 1
            eval_data.fn_sents[classification].append(text)


def find_sent_gold_substs(sent, doc):
    """@type doc: Document"""
    gold_substs = set()
    for substance in doc.highlighted_spans:
        for gold_span in doc.highlighted_spans[substance]:
            overlap = check_sent_overlap(gold_span.start, gold_span.stop, sent.span_in_doc_start, sent.span_in_doc_end)
            if overlap:
                gold_substs.add(substance)
    return gold_substs
