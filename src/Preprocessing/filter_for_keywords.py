# This script reads in a set of documents from a directory, and feeds them to KeywordHit module which checks
#    whether the document contains words of interest; anything related to smoking or tobacco.

from os import listdir
from os.path import isfile, join
from SystemUtilities.Configuration import *
from SystemUtilities.Globals import *
from DataModeling.DataModels import Document, Patient
from Extraction.KeywordSearch import KeywordSearch
from nltk.tokenize import sent_tokenize
from Preprocessing.get_docs_to_annotate import DataSplitter

def main():
    # Read in from folder containing all available data
    data_src = data_repo_dir
    data = load_data(data_src)
    documents = create_documents_from_data(data)
    patients = create_patients_from_documents(documents)

    docs_with_keywords = KeywordSearch.search_keywords(patients)

    # Based on Flor's divisions, derive list of documents that need annotation
    print("Generating list of documents that need annotations...")
    splitter = DataSplitter(docs_with_keyword_hits)
    splitter.write_notes_needing_annotation()
    print("Done.")

def load_data(data_src):
    print("Loading data...")
    # debug
    # data_src = "C:\Users\sdmorris\Documents\FHCRC\ExposureProject\Substance_IE_Data\mini_data"
    # data_src = "C:\Users\wlane\Documents\Substance_IE_Data\mini_output_corpus"
    # end debug

    file_list = [f for f in listdir(data_src) if isfile(join(data_src, f))]
    id_and_note = dict()
    for file in file_list:
        full_id = file
        with open(data_src + "/"+file) as f:
            content = f.read()
            id_and_note[full_id] = content
    return id_and_note  # returns dictionary of {doc_id : document_text}


def create_documents_from_data(data):
    print("Creating Documents from data...")
    documents = list()
    for id, text in data.iteritems():
        new_doc = Document(id, text)
        sent_tokenize_list = sent_tokenize(text.decode("utf-8"))
        new_doc.sent_list=sent_tokenize_list
        documents.append(new_doc)
    return documents


def create_patients_from_documents(documents):
    print ("Creating patients from documents...")
    patientId_docList = dict()
    for doc in documents:
        patient_id = doc.id.split("_")[0]
        if patient_id not in patientId_docList:
            patientId_docList[patient_id] = list()
        patientId_docList[patient_id].append(doc)

    # read through patients in dictionary and make patient objects for each
    patients = list()
    for id, doc_list in patientId_docList.iteritems():
        new_patient = Patient(id)
        new_patient.doc_list = doc_list
        patients.append(new_patient)
    return patients


if __name__ == '__main__':
    main()
