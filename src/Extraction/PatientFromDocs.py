from SystemUtilities.Globals import *
from DataModeling.DataModels import Event


def get_patient_level_info(patients):

    for patient in patients:
        # Get events
        find_patient_events(patient)

        # Get status
        get_patient_status(patient)

        # Get each attribute
        # TODO -- attribs from docs


def find_patient_events(patient):
    substances_in_docs = substances_found_in_docs(patient)

    for substance in substances_in_docs:
        patient.predicted_events.append(Event(substance))


def substances_found_in_docs(patient):
    substances_in_docs = set()
    for doc in patient.doc_list:
        for event in doc.predicted_events:
            substances_in_docs.add(event.substance_type)
    return substances_in_docs


def get_patient_status(patient):
    for pred_event in patient.predicted_events:
        chronological_docs = sort_docs_chronologically(patient.doc_list)
        pred_event.status = get_patient_subst_status(chronological_docs, pred_event.substance_type)


def sort_docs_chronologically(doc_list):
    sorted_docs = []
    # TODO -- sort_docs_chronologically to find patient status
    return sorted_docs


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
