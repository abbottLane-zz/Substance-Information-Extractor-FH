from SystemUtilities.Configuration import *
from Processing import *


def evaluate(patients):
    fn_sents = {}   # {event type : [sentences]}
    fp_sents = {}   # {event type : [sentences]}
    tp = 0
    fn = 0
    fp = 0

    # Track sentences with errors for areas of improvement
    for event_type in ML_CLASSIFIER_SUBSTANCES:
        fn_sents[event_type] = []
        fp_sents[event_type] = []

    # Evaluate each sentence
    for doc in patients.doc_list:
        for sent in doc.sent_list:
            tp, fp, fn = evaluate_sentence(sent, doc.highlighted_spans, fn_sents, fp_sents, tp, fp, fn)

    precision = float(tp) / float(tp + fp)
    recall = float(tp) / float(tp + fn)

    output_evaluation(precision, recall, fp_sents, fn_sents)


def evaluate_sentence(sent, doc, fn_sents, fp_sents, tp, fp, fn):
    gold_substs = find_sent_gold_substs(sent, doc)
    predicted_substs = [p.substance_type for p in sent.predicted_events]

    # Find true pos, false pos
    for classf in predicted_substs:
        if classf in gold_substs:
            tp += 1
        else:
            fp += 1
            fp_sents[classf].append(sent.text)
    # Find false neg
    for classf in gold_substs:
        if classf not in predicted_substs:
            fn += 1
            fn_sents[classf].append(sent.text)
    return tp, fp, fn


def find_sent_gold_substs(sent, doc):
    gold_substs = set()
    for substance in doc.highlighted_spans:
        for gold_span in doc.highlighted_spans[substance]:
            overlap = check_sent_overlap(gold_span.start, gold_span.stop, sent.span_in_doc_start, sent.span_in_doc_end)
            if overlap:
                gold_substs.add(substance)
    return list(gold_substs)


def output_evaluation(precision, recall, fp_sents, fn_sents):
    out_file = open(CLASSF_EVAL_FILENAME, "w")

    # Precision/recall
    out_file.write("\nClassifier Evaluation " + "\n---------------------\n")
    out_file.write("Precision: " + str(precision) + "\n")
    out_file.write("Recall: " + str(recall) + "\n\n")

    # Misclassified sentences
    out_file.write("<< FP Sentences >>\n")
    for event_type in fp_sents:
        out_file.write(event_type + "\n")
        for sent in fp_sents[event_type]:
            out_file.write(sent + "\n")

    out_file.write("<< FN Sentences >>\n")
    for event_type in fn_sents:
        out_file.write(event_type + "\n")
        for sent in fn_sents[event_type]:
            out_file.write(sent + "\n")

