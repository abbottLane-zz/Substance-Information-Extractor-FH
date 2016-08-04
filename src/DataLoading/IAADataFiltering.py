
def get_interannotated_docs(annotations):
    # Grab inter-annotated patients and throw out the rest
    mrn_filtered_docs, num_of_annotators = filter_by_mrn(annotations)

    # Grab inter-annotated docs and throw out the rest
    doc_filtered_docs, iaa_possible = filter_by_doc(mrn_filtered_docs)
    return doc_filtered_docs, iaa_possible, num_of_annotators


def filter_by_mrn(annotations):
    """ Grab the documents of MRNs which have been annotated by all annotators """
    annotators = annotations.keys()
    number_of_annotators = len(annotators)
    mrn_filtered_docs = {annotator: {} for annotator in annotators}  # {annotator: {doc_id: [Events]}}

    if number_of_annotators > 1:
        # Grab one annotator's MRNs and keep ones shared by all other annotators
        first_annotator_mrns = annotations[annotators[0]]
        for mrn in first_annotator_mrns:
            if is_fully_interannotated(mrn, annotations, annotators[1:]):
                grab_mrn_docs_per_annotator(annotators, mrn, annotations, mrn_filtered_docs)

    return mrn_filtered_docs, number_of_annotators


def is_fully_interannotated(mrn, annotations, other_annotators):
    interannotated = True
    for annotator in other_annotators:
        if mrn not in annotations[annotator]:
            interannotated = False
            break
    return interannotated


def grab_mrn_docs_per_annotator(annotators, mrn, annotations, mrn_filtered_docs):
    for annotator in annotators:
        mrn_docs = annotations[annotator][mrn]
        mrn_filtered_docs[annotator].update({doc: mrn_docs[doc] for doc in mrn_docs})


def filter_by_doc(mrn_filtered_docs):
    """ Grab the documents which have been annotated by all annotators """
    annotators = mrn_filtered_docs.keys()
    interannotated_docs = {}
    iaa_possible = False

    if len(annotators) > 1:
        first_annotator_docs = mrn_filtered_docs[annotators[0]]
        for doc in first_annotator_docs:
            if is_fully_interannotated(doc, mrn_filtered_docs, annotators[1:]):
                grab_interannotated_docs(annotators, doc, mrn_filtered_docs, interannotated_docs)
                iaa_possible = True

    return interannotated_docs, iaa_possible


def grab_interannotated_docs(annotators, doc_id, mrn_filtered_docs, interannotated_docs):
    interannotated_docs[doc_id] = {}
    for annotator in annotators:
        docs = mrn_filtered_docs[annotator]
        interannotated_docs[doc_id][annotator] = docs[doc_id]
