from SystemUtilities.Globals import *


def get_patient_level_info(patients):

    for patient in patients:
        # Get events
        # TODO -- events from docs

        # Get status
        get_patient_status(patient)

        # Get each attribute
        # TODO -- attribs from docs


def get_patient_status(patient):
    for pred_event in patient.predicted_events:
        chronological_docs = sort_docs_chronologically(patient.doc_list)
        pred_event.status = get_patient_subst_status(chronological_docs, pred_event.substance_type)


def sort_docs_chronologically(doc_list):
    sorted_docs = []
    # TODO
    raise NotImplementedError
    # return sorted_docs


def get_patient_subst_status(docs, substance):
    """ Recursively descend through chronologically sorted docs to determine patient level status by reasoning
    based on doc level statuses"""
    doc_status = docs[0].gold_events[substance].status
    previous_docs = docs[1:]

    if doc_status in POSITIVE_STATUSES or not previous_docs:
        patient_status = doc_status
    else:
        patient_status = patient_status_if_current_doc_non_or_unk(doc_status, previous_docs, substance)

    return patient_status


def patient_status_if_current_doc_non_or_unk(doc_status, previous_docs, substance):
    previous_status = get_patient_subst_status(previous_docs, substance)

    if doc_status == NON:
        if previous_status in POSITIVE_STATUSES:
            patient_status = FORMER
        else:
            patient_status = NON

    else:  # doc_status == UNKNOWN
        patient_status = previous_status

    return patient_status
