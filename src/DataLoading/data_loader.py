import os
from DataModeling.DataModels import Patient, Document, Sentence
import SystemUtilities.Configuration as config
import SystemUtilities.Globals
import re
from os import listdir
from os.path import isfile, join

def list_to_dict(list_files):
    annotation_dict = dict()
    for annotation_file in list_files:
        with open(annotation_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                id_label_pairs = line.split()
                id = id_label_pairs[0]
                label = id_label_pairs[1]
                annotation_dict[id] = label
    return annotation_dict

def load_gold_annotations(test_files_list, train_files_list):
    test_annotation_dict = dict()  # {doc_id : gold_label}
    train_annotation_dict = dict()  # {doc_id : gold_label}
    if len(test_files_list) > 0:
        test_annotation_dict = list_to_dict(test_files_list)
    if len(train_files_list) > 0:
        train_annotation_dict = list_to_dict(train_files_list)
    return test_annotation_dict, train_annotation_dict


def load_src_text(list_data_dir, test_data, train_data):
    # instead of opening every file in the repo folder, just open the ones we care about
    data_dict = dict() # {fileID : list_of_text_lines}
    for data_dir in list_data_dir:
        list_dir = os.listdir(data_dir)
        for filename in list_dir:
            base, ext = os.path.splitext(filename)
            if base in test_data or base in train_data: # If the file_id is in the env set
                with open(data_dir+filename, "r") as f:
                    doc_lines = f.readlines()
                    data_dict[base] = doc_lines
    return data_dict


def data_and_annotations_to_patient(ann_dict, data_dict):
    # Create a dictionary of { patientID : [list of docs] }
    patients = dict()
    for document_id in ann_dict.keys():
        if "-" not in document_id:  # then its a person
            patients[document_id] = list()

    # loop through patients and assign their documents
    for document_id in ann_dict.keys():
        if "-" in document_id:
            pid_did = re.split("-", document_id)
            pid = pid_did[0]
            if patients.has_key(pid):
                patients[pid].append((document_id, data_dict[document_id]))
            else:
                print("HEyy! Found a doc belonging to an unknown patient!")
    return patients


def build_data_models(data_dict, test_ann_dict, train_ann_dict):

    ## Get TRAINING patients
    training_patients = data_and_annotations_to_patient(train_ann_dict, data_dict)

    ## Get TESTING patients
    testing_patients = data_and_annotations_to_patient(test_ann_dict, data_dict)

    # TODO: finish building objects
    tmp=8
    pass


def main():
    from optparse import OptionParser
    parser = OptionParser(__doc__)
    options, args = parser.parse_args()

    if len(args) == 0:
        ## Load annotations into dict()
        test_data_folders, train_data_folders = config.get_environment_gold_data(config.ENV)
        test_ann_dict, train_ann_dict = load_gold_annotations(test_data_folders, train_data_folders)

        ## Load src text into dict
        raw_data = config.get_environment_text_data(config.ENV)
        data_dict = load_src_text(raw_data, test_ann_dict, train_ann_dict)

        ## Build data objects
        training_patients, testing_patients = build_data_models(data_dict, test_ann_dict, train_ann_dict)

if __name__ == '__main__':
    main()