def extract_sentences_from_patients(patients):
    sentences=list()
    for patient in patients:
        for doc in patient.doc_list:
            for sent in doc.sent_list:
                sentences.append(sent)
    return sentences


def classify_sentence_status(patients):
    sentences = extract_sentences_from_patients(patients)
    tmp = 0
    return None