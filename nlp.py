"""
Core framework class for NLP Comparative Analysis

"""
from collections import Counter, defaultdict
import nltk
from nltk.corpus import stopwords
import io
from nltk.tokenize import word_tokenize


class Nlp:
    """ core framework for NLP comparative analysis

    Attributes:
        data (dict): dictionary managing data about the different texts that we register with the framework
        viz (dict): dictionary that maps the name of the visualization to the visualization function
    """

    def __init__(self):
        self.data = defaultdict(dict)
        self.viz = {}

    @staticmethod
    def _default_parser(filename):
        """ Parser that cleans out file based on stop words and gets results (interested data about the words)

        Args:
            filename (str): name of interested filename

        Returns:
            results (dict): key being what data collected and value being the data
        """
        # initialize empty list to store words
        words = []

        # load the stop words
        stop_words = Nlp._load_stop_words()

        # open and read the interested file
        text_file = open(filename, 'r')
        rows_of_text = text_file.readlines()

        # filtering the file
        for row in rows_of_text:
            # remove all break lines
            row = row.replace('\n', '')
            # separate the words from each row in the txt file
            row_words = row.split(' ')
            for word in row_words:
                # make all the letters lower case
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

        Args:
            label (str): unique label for a text file that we parsed
            results (dict): the data extracted from the file as a dictionary attribute--> raw data
        """
        for k, v in results.items():
            self.data[k][label] = v

    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework

        Args:
            filename(str): name of interested file
            label(str): optional label for file
            parser(str): optional type of parser to be used
        """
        # do default parsing of standard .txt file
        if parser is None:
            results = Nlp._default_parser(filename)
        else:
            # NEED TO FIGURE OUT WHAT PARSER IS? IS IT ANOTHER FUNCTION?
            results = parser(filename)
        if label is None:
            label = filename

        # Save/integrate the data we extracted from the file into the internal state of the framework
        self._save_results(label, results)


    @staticmethod
    # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    def _load_stop_words(stopfile=None):
        """ Clean the data by removing stop words

        Args:
            stopfile (str): optional txt file containing stop words, or common words that will get filtered
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

            # filtering the stop file
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

    def load_visualization(self, name, vizfunc, *args, **kwargs):
        """ Integrate visualization into internal state

        Args:
            name (str): name of visualization
            vizfunc (function): name of function to execute the visualization
            *args: unlimited number of defined parameters
            **kwargs: unlimited number of undefined parameters
        """
        self.viz[name] = (vizfunc, args, kwargs)

    def visualize(self, name=None):
        """ Call the vizfunc to plot the visualization

        Args:
            name (str): optional parameter for name of visualization
        """
        # run all
        if name is None:
            for _, v in self.viz.items():
                vizfunc, args, kwargs = v
                vizfunc(self.data, *args, **kwargs)
        else:
            # run only the named visualization
            vizfunc, args, kwargs = self.viz[name]
            vizfunc(self.data, *args, **kwargs)
