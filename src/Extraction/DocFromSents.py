from SystemUtilities.Globals import STATUS_HIERARCHY, UNKNOWN


def get_doc_level_status(patients):
    """ Get document level status from sentence level statuses """

    for patient in patients:
        for doc in patient.doc_list:
            for doc_event in doc.predicted_events:   # TODO -- will this be populated???
                substance = doc_event.substance_type

                sentence_level_statuses = get_sent_level_statuses_for_doc(doc, substance)
                doc_status = doc_level_status(sentence_level_statuses)

                doc_event.status = doc_status


def get_sent_level_statuses_for_doc(doc, substance):
    """ Get all values of status in the doc's sentences for the given substance """
    sentence_level_statuses = set()

    for sent in doc.sent_list:
        for event in sent.predicted_events:
            if event.substance_type == substance:
                sentence_level_statuses.add(event.status)

    return sentence_level_statuses


def doc_level_status(sentence_level_statuses):
    doc_status = UNKNOWN

    # Go through precedence-ordered list of statuses and take the first one found
    for status in STATUS_HIERARCHY:
        if status in sentence_level_statuses:
            doc_status = status
            break

    return doc_status
