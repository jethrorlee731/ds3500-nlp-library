"""
Core framework class for NLP Comparative Analysis

"""
from collections import Counter, defaultdict
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
        words = []

        # load the stop words
        stop_words = Nlp._load_stop_words()

        # open and read the txt file
        text_file = open(filename, 'r')
        rows_of_text = text_file.readlines()

        # filtering the file
        for row in rows_of_text:
            # remove all break lines
            row = row.replace('\n', '')
            # separate the words from each row in the txt file
            row_words = row.split(' ')
            for word in row_words:
                word = word.lower()
                # only include words in the word count if they aren't a stop word
                # filter out blank words and possible non-words (e.g., "words" that start with a number)
                if word not in stop_words and word != '' and word[0].isalpha():
                    # remove punctuation from the end of words
                    if not word[-1].isalpha():
                        word = word[:-1]
                    words.append(word)
        # close the file
        text_file.close()

        # create a dictionary with the frequency of each unique word in a file as well as the word count of the file
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
    def _load_stop_words(stopfile=None):
        """ Clean the data by removing stop words
        Args:
            stopfile (txt): a file containing stop words, or common words that will get filtered out of the txt file
        Returns:
            stop_words (list): list of stopwords based on NLTK library
        """
        if stopfile is None:
            nltk.download('stopwords')
            stop_words = list(stopwords.words('english'))
        else:
            stop_words = []

            # open and read the stop file
            stop_file = open(stopfile, 'r')
            rows_of_text = stop_file.readlines()

            # filtering the file
            for row in rows_of_text:
                # remove all break lines
                row = row.replace('\n', '')
                # separate the words from each row in the txt file
                row_words = row.split(' ')
                for word in row_words:
                    word = word.lower()
                    # filter out blank words and possible non-words (e.g., "words" that start with a number)
                    if word != '' and word[0].isalpha():
                        # remove punctuation from the end of words
                        if not word[-1].isalpha():
                            word = word[:-1]
                        stop_words.append(word)
            # close the file
            stop_file.close()

        return stop_words

    def wordcount_sankey(self, word_list=None, k=5):
        """ Maps each text to words on a Sankey diagram, where the thickness of the line is the frequency of that word
        Args:
            word_list (list): a list containing a set of words to be shown on the diagram
            k (int): the union of the k most common words across each file
        Returns:
            stop_words (list): list of stopwords based on NLTK library
        """
        word_count_dict = self.data['wordcount']

        texts = []
        all_words = []
        all_counts = []

        for text, word_count in word_count_dict.items():
            word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                                reverse=True)}
            words = list(word_count.keys())
            if word_list is None:
                if k is not None:
                    words = words[:k+1]
            else:
                words = [word for word in words if word in word_list]
            counts = list(word_count.values())
            counts = counts[:k+1]
            text = [text] * len(words)

            texts += text
            all_words += words
            all_counts += counts

        word_count = list(zip(all_words, all_counts, texts))
        df_word_counts = pd.DataFrame(word_count, columns=['Word', 'Counts', 'Text'])
        print(df_word_counts)
        sk.make_sankey(df_word_counts, 0, 'Text', 'Word', vals=df_word_counts['Counts'])
