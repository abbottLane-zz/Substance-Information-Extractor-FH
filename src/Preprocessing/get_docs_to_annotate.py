import SystemUtilities.Configuration as c
import SystemUtilities.Globals as g
import os
import openpyxl
import collections


def write_unannotated_info_to_file(unannotated_documents):
    with open(c.SUBSTANCE_IE_DATA_FOLDER + "docs_to_annotate.txt", "w") as f:
        for doc in unannotated_documents:
            f.write(doc.id+"\n")
    pass


class DataSplitter:
    def __init__(self, docs_with_keywords):
        self.docs_with_keywords_list = docs_with_keywords
        self.doc_test_dict = dict()
        self.doc_dev_dict = dict()
        self.doc_train_dict = dict()
        self.patients_test_dict = dict()
        self.patients_dev_dict = dict()
        self.patients_train_dict = dict()

    def split_into_dev_test_train(self):
        self.get_splits()
        pass

    def get_unannotated_documents(self, all_keyword_documents):
        unannotated_docs = list()
        for doc in all_keyword_documents:
            doc.id = doc.id.replace("_", "-")  # Our ids have '_', Flors have '-'
            if not doc.id in self.doc_test_dict.keys() \
                    and not doc.id in self.doc_dev_dict.keys() \
                    and not doc.id in self.doc_train_dict.keys():
                unannotated_docs.append(doc)
        return unannotated_docs

    def get_list_of_documents_to_annotate(self):
        # all of the .self attributes have been populated by this point, use them to sort the new data

        unannotated_documents = self.get_unannotated_documents(self.docs_with_keywords_list)
        return unannotated_documents

    def populate_dir_dict(self, doc_dict, patients_dict, dirs):
        doc_gold_dir = dirs[0]
        patients_gold_dir = dirs[1]

        with open(doc_gold_dir) as d:
            lines = d.readlines()
        for line in lines:
            id_label = line.split()
            id = id_label[0]
            label = id_label[1]
            doc_dict[id] = label

        with open(patients_gold_dir) as d:
            lines = d.readlines()
        for line in lines:
            id_label = line.split()
            id = id_label[0]
            label = id_label[1]
            patients_dict[id] = label
        pass

    def get_splits(self):
        doc_dev_gold_dir = c.doc_dev_gold_dir
        doc_test_gold_dir = c.doc_test_gold_dir
        doc_train_gold_dir = c.doc_train_gold_dir
        patients_test_gold_dir = c.patients_test_gold_dir
        patients_train_gold_dir = c.patients_train_gold_dir
        patients_dev_gold_dir = c.patients_dev_gold_dir

        dev_dirs = [doc_dev_gold_dir, patients_dev_gold_dir]
        test_dirs = [doc_test_gold_dir, patients_test_gold_dir]
        train_dirs = [doc_train_gold_dir, patients_train_gold_dir]

        self.populate_dir_dict(self.doc_dev_dict, self.patients_dev_dict, dev_dirs)
        self.populate_dir_dict(self.doc_test_dict, self.patients_test_dict, test_dirs)
        self.populate_dir_dict(self.doc_train_dict, self.patients_train_dict, train_dirs)

        documents_needing_annotation = self.get_list_of_documents_to_annotate()
        write_unannotated_info_to_file(documents_needing_annotation)
