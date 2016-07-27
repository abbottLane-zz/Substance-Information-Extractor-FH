import csv
from nltk.tokenize import sent_tokenize
from DataModeling.DataModels import Document, Event, Patient, Sentence
from SystemUtilities import Configuration
from os import listdir
from os.path import isfile, join


def main():
    print "Loading patient-level gold labels ..."
    patient_tob_gold_labels = Configuration.patients_all_gold_dir
    patient_alc_gold_labels = None

    print "Loading dev/train/test document splits ..."
    dev_documents = load_split(Configuration.dev_csv)
    training_documents = load_split(Configuration.train_csv)
    testing_documents = load_split(Configuration.test_csv)

    print "Loading dev/train/test patient splits ..."
    dev_patients = load_patients(dev_documents, patient_tob_gold_labels, patient_alc_gold_labels)
    training_patients = load_patients(training_documents, patient_tob_gold_labels, patient_alc_gold_labels)
    testing_patients = load_patients(testing_documents, patient_tob_gold_labels, patient_alc_gold_labels)

    print "Loading sentence-level annotations ..."
    # Load Sentence-level annotations, if available
    sentence_level_annotations_dir = Configuration.flor_sentence_level_annotations_dir
    sent_ann_dict = load_sentence_annotations(sentence_level_annotations_dir)

    print "Setting sentence-level annotations ..."
    # Set sentence-level annotations
    set_sentence_level_annotations(dev_patients, sent_ann_dict)
    set_sentence_level_annotations(training_patients, sent_ann_dict)
    set_sentence_level_annotations(testing_patients, sent_ann_dict)

    print "Patient objects ready for processing."
    print "Done."
    # TODO: Patient objects for dev/test/train are fully populated above. Do something with them.



def set_sentence_level_annotations(patients, sent_ann_dict):
    for patient in patients:
        for doc in patient.doc_list:
            for sentence in doc.sent_list:
                if sentence.text.rstrip() in sent_ann_dict:
                    substype = sent_ann_dict[sentence].split("_")[0]
                    sent_label = sent_ann_dict[sentence][1]
                    evntObj = Event(substype)
                    evntObj.status = sent_label
                    sentence.predicted_events.append(evntObj)
    pass


def load_sentence_annotations(sentence_level_annotations_dir):
    sent_label_dict = dict()
    labels = {'C': "CURRENT", 'P': "PAST", 'U': "UNKNOWN", 'S': "SMOKER", "N": "NON", 'c': "CURRENT", 'p': "PAST",
              'u': "UNKNOWN", 's': "SMOKER", "n": "NON"}

    onlyfiles = [f for f in listdir(sentence_level_annotations_dir) if isfile(join(sentence_level_annotations_dir, f))]
    for subsType in onlyfiles:  # b/c sentence-level labels are organized into files by type (cig, alc, drug, etc)
        with open(sentence_level_annotations_dir + "\\" + f, "rb") as file:
            lines = file.readlines()
        for line in lines:
            tokens = line.split()
            label = tokens[0]
            sentence = line[2:]
            if label in labels:
                sent_label_dict[sentence.rstrip()] = subsType + "_" + labels[label]
    return sent_label_dict


def read_csv(filepath):
    ID = "ID"
    TEXT = "TEXT"
    TOB_GOLD = "TOB_GOLD_LABEL"
    ALC_GOLD = "ALC_GOLD_LABEL"
    document_tuples = list()
    with open(filepath, "rb") as csv_file:
        note_reader = csv.reader(csv_file)
        line_number = 0
        for row in note_reader:  # each row is a document and its metadata
            if line_number == 0:  # its not the header
                headers = dict((k, v) for v, k in enumerate(row))
            else:
                note_text = row[headers.get(TEXT)]
                id = row[headers.get(ID)]
                tob_label = row[headers.get(TOB_GOLD)]
                alc_label = row[headers.get(ALC_GOLD)]
                document_tuples.append(tuple([id, note_text, tob_label, alc_label]))
            line_number += 1
    return document_tuples


def split_document_into_sentences(doc):
    text = doc.text
    sent_tokenize_list = sent_tokenize(text)

    sentence_object_list = list()
    for sent in sent_tokenize_list:
        sentObj = Sentence(doc.id, sent)
        sentence_object_list.append(sentObj)
    return sentence_object_list


def load_split(split_csv_path):
    """ Returns a list of document objects for the given split """
    document_tuples = read_csv(split_csv_path)
    document_objs = list()
    for tup in document_tuples:
        doc_id = tup[0]
        text = tup[1]
        tob_gold_label = tup[2]
        alc_gold_label = tup[3]
        doc = Document(doc_id, text)

        if tob_gold_label != "UNKNOWN":
            # Populate Tobacco Events
            tob_event = Event("Tobacco")
            tob_event.status = tob_gold_label.rstrip()
            if tob_event.status != "":
                doc.gold_events.append(tob_event)
        if alc_gold_label != "UNKNOWN":
            # Populate Alcohol Events
            alc_event = Event("Alcohol")
            alc_event.status = alc_gold_label.rstrip()
            if alc_event.status != "":
                doc.gold_events.append(alc_event)

        # Populate sentence objects in the doc object
        sentences = split_document_into_sentences(doc)
        doc.sent_list = sentences

        document_objs.append(doc)
    return document_objs


def load_patient_labels(patient_gold_labels_path):
    pid_label = dict()
    if patient_gold_labels_path is not None:
        with open(patient_gold_labels_path, "rb") as file:
            lines = file.readlines()
        for line in lines:
            id_label = line.split()
            pid_label[id_label[0]] = id_label[1]
    return pid_label


def load_patients(documents, patient_tob_gold_labels_path, patient_alc_gold_labels_path):
    """ Returns a list of patient objects populated with their respective documents """
    # Load gold labels
    pid__tob_goldLabel = load_patient_labels(patient_tob_gold_labels_path)
    pid__alc_goldLabel = load_patient_labels(patient_alc_gold_labels_path)

    # Build {patient : [docObj1, docObj2, ..,]} dictionary
    pid_listdocs_dict = dict()
    for doc in documents:
        pid = doc.id.split("-")[0]
        if pid in pid_listdocs_dict:
            pid_listdocs_dict[pid].append(doc)
        else:
            pid_listdocs_dict[pid] = list()
            pid_listdocs_dict[pid].append(doc)

    # Build list of patient objects
    patient_objects = list()
    for pid, doc_list in pid_listdocs_dict.iteritems():
        pat = Patient(pid)
        pat.doc_list = doc_list
        patient_objects.append(pat)

        if patient_tob_gold_labels_path is not None:
            # Populate Tobacco Events
            tob_event = Event("Tobacco")
            tob_event.status = pid__tob_goldLabel[pid].rstrip()
            if tob_event.status != "":
                pat.gold_events.append(tob_event)
        if patient_alc_gold_labels_path is not None:
            # Populate Alcohol Events
            alc_event = Event("Alcohol")
            alc_event.status = pid__alc_goldLabel[pid].rstrip()
            if alc_event.status != "":
                pat.gold_events.append(alc_event)
    return patient_objects


if __name__ == '__main__':
    main()
