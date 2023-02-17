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
        stop_words = Nlp._load_stop_words()

        text_file = open(filename, 'r')
        rows_of_text = text_file.readlines()
        words = []
        for row in rows_of_text:
            row = row.replace('\n', '')
            row_words = row.split(' ')
            for word in row_words:
                word = word.lower()
                if word not in stop_words and word != '':
                    words.append(word)
        text_file.close()

        results = {
            'wordcount': Counter(words),
            'numwords': len(words)
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
        # do default parsing of standard .txt file
        if parser is None:
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
    def _load_stop_words():
        """ Clean the data by removing stop words
        Args:
            None
        Returns:
            stop_words (list): list of stopwords based on NLTK library
        """
        nltk.download('stopwords')
        stop_words = list(stopwords.words('english'))

        # PROBABLY DON'T NEED THE COMMENTED LINES BELOW BECAUSE IT IS ADDRESSED IN THE DEFAULT_PARSER FUNCTION
        # file1 = open(filename)
        #
        # # Use this to read file content as a stream:
        # line = file1.read()
        # words = line.split()
        # for r in words:
        #     if r not in stop_words:
        #         appendFile = open('filtered'+filename, 'a')
        #         appendFile.write(" "+r)
        #         appendFile.close()

        return stop_words

    def wordcount_sankey(self, word_list=None, k=5):
        #    df_word_counts = pd.DataFrame(self.data)
        #    sk.make_sankey(df_word_counts, threshold=0, df_word_counts[0],  vals=None, **kwargs )
        pass
