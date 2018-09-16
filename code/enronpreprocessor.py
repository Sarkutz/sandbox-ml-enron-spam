import os

stop_words = set()

def get_stop_words(path):
    stop_words = set()
    with open(path) as f:
        for word in f.read().split("\n")[:-1]:
            for token in word.split("'"):
                stop_words.add(token)
    return stop_words


def should_filter(token):
    # noisy_punctuations = ".,;:!?&\/$%\"`'()"  # Orig
    # noisy_punctuations = ".,;:!?&\/$%\"`'()-"
    noisy_punctuations = ".,;:?&\/$%\"`'()-"
    if token in noisy_punctuations:
        return True

    if token.lower() in stop_words:
        return True
    

def preprocess(clas, filepath, text, cb):
    relevant_tokens = [token for token in text.split() if not should_filter(token)]
    cb(clas=clas, doc_name=filepath, tokens=relevant_tokens)


def process_dataset(datasetpath, cb, debug):
    classes = ["ham", "spam"]
    for clas in classes:
        dirpath = datasetpath + clas + "/"
        if "print_dirs" in debug:
            print("DIRECTORY: " + dirpath)

        for filename in os.listdir(dirpath):
            filepath = dirpath + filename

            if "print_files" in debug:
                print("FILE: " + filepath)

            with open(filepath) as f:
                preprocess(clas, filepath, f.read(), cb)

            if "run_onefile_only" in debug:
                break


def run(datasets, cb, debug):
    global stop_words
    stop_words = get_stop_words("../dat/english.stop.txt")

    for dataset in datasets:
        datasetpath = "../dat/enron/" + dataset + "/"
        process_dataset(datasetpath, cb, debug)
