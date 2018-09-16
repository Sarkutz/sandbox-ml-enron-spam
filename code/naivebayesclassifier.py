import math
import sys
epsilon = sys.float_info[8]

ix_doc_freq = 0
ix_word_freq = 1

def flattened_str(l, sep="\t"):
    # return reduce(lambda x, y: str(x) + sep + str(y), l)
    return sep.join([str(x) for x in l])


class NaiveBayesClassifier(object):

    def __init__(self, classes):
        class2class_ix = [ (x[1], x[0]) for x in enumerate(classes) ]
        self.__classes = dict(class2class_ix)

        # TODO: Is there any benefit of using a list (instead of dict) for word
        # frequencies?
        self.__freq_table = {}

        self.__class_freq = [ epsilon for _ in range(len(classes)) ]
        self.__total_words = 0


    def train(self, doc_name, word, clas):
        class_ix = self.__classes[clas]

        if self.__freq_table.has_key(word):
            # DocFreq
            self.__freq_table[word][ix_doc_freq].add(doc_name)
            
            # WordFreq
            self.__freq_table[word][ix_word_freq][class_ix] += 1

        else:
            l = [-1, -1]

            # DocFreq
            l[ix_doc_freq] = set([doc_name])

            # WordFreq
            l[ix_word_freq] = [ epsilon for _ in range(len(self.__classes)) ]
            l[ix_word_freq][class_ix] += 1

            self.__freq_table[word] = l

        # ClassFreq
        self.__class_freq[class_ix] += 1
        self.__total_words += 1
        

    def classify(self, text):
        if self.__total_words <= 0:
            print("Must train before classify")
            return None

        ll_map = {}
        max_log_likelyhood, predicted_class = 0, ""
        for clas in self.__classes:
            class_ix = self.__classes[clas]
            class_freq = self.__class_freq[class_ix]
            log_prob_class = math.log(class_freq / self.__total_words)

            class_ix_2 = 1 if class_ix == 0 else 0
            class_freq_2 = self.__class_freq[class_ix_2]

            log_likelyhood = log_prob_class
            for token in text.split():
                if self.__freq_table.has_key(token):
                    word_freq = self.__freq_table[token][ix_word_freq][class_ix]
                    log_prob_word = math.log(word_freq / class_freq)

                    word_freq_2 = self.__freq_table[token][ix_word_freq][class_ix_2]
                    log_prob_word_2 = math.log(word_freq_2 / class_freq_2)  # TODO

                    if abs(log_prob_word - log_prob_word_2) < 0.1:
                        continue

                    log_likelyhood += log_prob_word

            ll_map[clas] = log_likelyhood
            # print("Log Likelyhood of {clas} = {ll}".format(clas=clas, ll=log_likelyhood))

            if max_log_likelyhood == 0 or max_log_likelyhood < log_likelyhood:
                max_log_likelyhood, predicted_class = log_likelyhood, clas

        return predicted_class, ll_map


    def __str__(self):
        sep = "\t"
        classes = sorted(self.__classes, key=lambda x: self.__classes[x])
        header = "NaiveBayesClassifier{sep}DocFreq{sep}{classes}".format(
                sep=sep, classes=flattened_str(classes))

        body = ""
        for word in self.__freq_table:
            freq_line = self.__freq_table[word]
            doc_freq = len(freq_line[ix_doc_freq])
            line = "{word}{sep}{doc_freq}{sep}{word_freqs}\n".format(
                    sep=sep, word=word, doc_freq=doc_freq,
                    word_freqs=flattened_str(freq_line[ix_word_freq]))
            body = body + line

        footer = "ClassFreq{sep}{class_freq}{sep}total_words={total_words}".format(
                sep=sep, class_freq=flattened_str(self.__class_freq),
                total_words=self.__total_words)

        return "\n".join([header, body, footer])

    def print_freqs(self, tokens):
        print("Token{sep}DocFreq{sep}LogProbSpam{sep}LogProbHam{sep}word_diff".format(
            sep="\t"))
        for token in tokens:
            if self.__freq_table.has_key(token):
                freq_line = self.__freq_table[token]
                doc_freq = len(freq_line[ix_doc_freq])
                word_freqs = freq_line[ix_word_freq]
                ix_spam = self.__classes["spam"]
                ix_ham = self.__classes["ham"]
                log_prob_spam = math.log(word_freqs[ix_spam] /
                        self.__class_freq[ix_spam])
                token_prob_ham = math.log(word_freqs[ix_ham] /
                        self.__class_freq[ix_ham])
                print("{token}{sep}{df}{sep}{log_prob_spam}{sep}{log_prob_ham}{sep}{diff}".format(
                    sep="\t", token=token, df=doc_freq,
                    log_prob_spam=log_prob_spam, log_prob_ham=token_prob_ham,
                    diff=abs(log_prob_spam-token_prob_ham)))

