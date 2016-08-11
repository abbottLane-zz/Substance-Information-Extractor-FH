import subprocess
import re
from SentenceTokenizer import strip_sec_headers_tokenized_text

features = [
    "useClassFeature=true",
    "useWord=true",
    "useNGrams=true",
    "noMidNGrams=true",
    "useDisjunctive=true",
    "maxNGramLeng=3",
    "usePrev=true",
    "useNext=true",
    "useSequences=true",
    "usePrevSequences=true",
    "maxLeft=1",
    "useTypeSeqs=true",
    "useTypeSeqs2=true",
    "useTypeySequences=true",
    "wordShape=chris2useLC"
]

entity_types = [
    "Amount",
    "Duration",
    "QuitDate",
    "QuitTimeAgo",
    "QuitAge",
    "SecondhandAmount"
]


def train(training_doc_objs, path="EntityExtractor/",
          stanford_ner_path="/home/wlane/stanford-ner-2015-04-20/stanford-ner.jar",
          train_script_name="train_model.sh"):
    global features
    global entity_types
    for type in entity_types:
        if type != "Status":
            train_file_name = path + "Train-Files/" + "train-" + type + ".tsv"
            prop_file_name = path + "Prop-Files/" + type + ".prop"
            model_name = path + "Models/" + "model-" + type + ".ser.gz"
            create_train_file(training_doc_objs, train_file_name, type)
            create_prop_file(prop_file_name, train_file_name, features, model_name)
            train_model(stanford_ner_path, prop_file_name, path + train_script_name)


def create_train_file(training_doc_objs, train_file_name, type):
    """
    Sorry about the crazy embedded FOR loops and indents.
    I will modularize better to make it prettier.
    """
    train_file = open(train_file_name, 'w')
    for doc in training_doc_objs:
        doc_obj = training_doc_objs[doc]
        for sent_obj in doc_obj.get_sentence_obj_list():
            if sent_obj.has_substance_abuse_entity():
                sentence = sent_obj.sentence
                entity_set = sent_obj.set_entities
                sent_offset = sent_obj.begin_idx

                for match in re.finditer("\S+", sentence):
                    start = match.start()
                    end = match.end()
                    pointer = sent_offset + start
                    word = match.group(0).rstrip(",.:;")
                    if word not in {"SOCIAL", "HISTORY", "SUBSTANCE",
                                    "ABUSE"}:  # see tokenizer in utils, they must both match
                        train_file.write(word)
                        # Debug line
                        # train_file.write("[" + str(pointer) + "," + str(sent_offset + match.end()) + "]")
                        train_file.write("\t")
                        answer = "0"
                        debug_str = ""
                        for entity in entity_set:
                            if answer != "0":
                                break
                            if entity.is_substance_abuse():
                                attr_dict = entity.dict_of_attribs
                                for attr in attr_dict:
                                    attr_start = int(attr_dict[attr].span_begin)
                                    attr_end = int(attr_dict[attr].span_end)
                                    if attr_dict[attr].type == type and \
                                                            attr_start <= pointer < attr_end:
                                        answer = type
                                        # Debug lines
                                        # answer += "\t" + attr_dict[attr].text +\
                                        #          "[" + str(attr_start) +\
                                        #          "," + str(attr_end) + "]"
                                        debug_str = "--- Sent obj start index: " + str(sent_offset) + "\n" + \
                                                    "--- Match obj start index: " + str(start) + "\n" + \
                                                    "--- Match obj end index: " + str(end) + "\n" + \
                                                    "--- Pointer index: " + str(sent_offset) + " + " + \
                                                    str(start) + " = " + str(pointer) + "\n" + \
                                                    "--- Attr start index: " + str(attr_start) + "\n" + \
                                                    "--- Attr end index: " + str(attr_end) + "\n"
                                        break
                        train_file.write(answer + "\n")
                        # Debug line
                        # train_file.write(debug_str)
                        # print(debug_str)

    train_file.close()


def create_prop_file(prop_file_name, train_file_name, features, model_name):
    prop_file = open(prop_file_name, 'w')
    prop_file.write("trainFile = " + train_file_name + "\n")
    prop_file.write("serializeTo = " + model_name + "\n")
    # prop_file.write("map = word=0,answer=1,temp=2,method=3,type=4,amount=5,freq=6,hist=7\n")
    prop_file.write("map = word=0,answer=1\n")
    for feat in features:
        prop_file.write(feat + "\n")
    prop_file.close()


def train_model(stanford_ner_path, prop_file_name, train_script_name):
    subprocess.call(["./" + train_script_name + " " + stanford_ner_path + " " + prop_file_name], shell=True)
