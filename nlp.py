"""
Core framework class for NLP Comparative Analysis

"""
from collections import Counter, defaultdict
import random as rnd
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd
import nltk
from nltk.corpus import stopwords
import io
from nltk.tokenize import word_tokenize

class Nlp:

    def __init__(self):
        # manage data about the different texts that we register with the framework
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        # incorrect implementation of a direct parser
        # enter code for the parser here
        results = {
            'wordcount': Counter('to be or not to be'.split(' ')),
            'numwords': rnd.randrange(10, 50)
        }

        return results

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label: unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute--> raw data
        """
        for k, v in results.items():
            self.data[k][label] = v

    # parser only works with this specific filename you're registering
    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework """
        if parser is None:  # do default parsing of standard .txt file
            results = Nlp._default_parser(filename)
        else:
            results = parser(filename)
        if label is None:
            label = filename

        # Save/integrate the data we extracted from the file into the internal state of the framework
        self._save_results(label, results)

    # def compare_num_words(self):
    #     num_words = self.data['numwords']
    #     for label, nw in num_words.items():
    #         plt.bar(label, nw)
    #     plt.show()

    @staticmethod
    # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    def load_stop_words(filename):
        stop_words = set(stopwords.words('english'))
        file1 = open(filename)

        # Use this to read file content as a stream:
        line = file1.read()
        words = line.split()
        for r in words:
            if not r in stop_words:
                appendFile = open('filteredtext.txt', 'a')
                appendFile.write(" " + r)
                appendFile.close()


                # I THINK WHAT YOU WROTE BELOW ONLY SPLITS THE WORDS BY A COMMA, IT DOESN'T ACTUALLY REMOVE THE STOP WORDS
        # stop_word_file = open(stopfile, 'r')
        # stop_words = stop_word_file.read()
        # stop_words = stop_words.split(',')
        # stop_word_file.close()

        return stop_words

    def wordcount_sankey(self, word_list=None, k=5):
        df_word_counts = pd.DataFrame(self.data)
        sk.make_sankey(df_word_counts, threshold=0, df_word_counts[0],  vals=None, **kwargs )
