#!/usr/bin/env python

import sys
import naivebayesclassifier as nbc
import enronpreprocessor as epp

global model
global debug
"""
Possible values for debug
["print_tokens", "print_files", "print_dirs", 
        "print_model", "print_predictions", "print_stopwords",
        "run_onefile_only", "run_train_only", "run_print_freqs"]
"""
sep = "\t"

def trainer(clas, doc_name, tokens):
    global debug, sep

    for token in tokens:
        if "print_tokens" in debug:
            print("TOKEN{sep}{clas}{sep}{token}{sep}{doc_name}".format(
                sep=sep, clas=clas, doc_name=doc_name, token=token))

        model.train(doc_name, token, clas)
    

def tester(clas, doc_name, tokens):
    global model, sep
    text = " ".join(tokens)
    predicted_class, ll_map = model.classify(text)
    if "print_predictions" in debug:
        print("{ok}{sep}{pred}{sep}{true}{sep}{ll_spam}{sep}{ll_ham}{sep}{doc}".format(
            sep=sep, ok=clas==predicted_class, doc=doc_name, true=clas,
            pred=predicted_class, ll_spam=ll_map["spam"], ll_ham=ll_map["ham"]))


def train():
    global model, debug
    model = nbc.NaiveBayesClassifier(["spam", "ham"])

    train_datasets = ["enron1", "enron2", "enron3", "enron4", "enron5"]
    epp.run(train_datasets, trainer, debug)
    if "print_model" in debug:
        print(model);


def test():
    global model, sep, debug

    if "print_predictions" in debug:
        print("Okay{sep}Pred{sep}True{sep}LogProbSpam{sep}LogProbHam{sep}DocName".format(
            sep=sep))

    test_datasets = ["enron6"]
    epp.run(test_datasets, tester, debug)

    
def print_token_freqs():
    filename = sys.argv[1]
    # with open("../dat/enron6/ham/3859.2001-06-27.lokay.ham.txt") as f:
    with open(filename) as f:
        tok = [x for x in f.read().split()]
    model.print_freqs(tok)


def main():
    global debug

    if "print_stopwords" in debug:
        sw = epp.get_stop_words("../dat/english.stop.txt")
        print(sw)
        return

    train()
    if "run_train_only" in debug:
        return

    if "run_print_freqs" in debug:
        print_token_freqs()
        return

    test()


if __name__ == "__main__":
    global debug
    debug = ["print_predictions"]
    main()
