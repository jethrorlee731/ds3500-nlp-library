"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

nlp.py: Core framework class for NLP Comparative Analysis
"""

from collections import Counter, defaultdict
from nltk.corpus import stopwords
import nlp_parsers as nlp_par
from exception import *


class Nlp:
    """ core framework for NLP comparative analysis

    Attributes:
        data (dict): dictionary managing data about the different texts that we register with the framework
        viz (dict): dictionary that maps the name of the visualization to a visualization function
    """

    def __init__(self):
        self.data = defaultdict(dict)
        self.viz = {}

    @staticmethod
    def _data_results(clean_words):
        """ Return data results based on the words

        Args:
            clean_words (list): list of clean words
        Returns:
            results (dict): dictionary with data about the inputted words
        """
        # make sure the inputted parameters are valid based on their type
        assert type(clean_words) == list, 'Clean words must be consolidated into a list'
        for word in clean_words:
            assert type(word) == str, 'Clean word list must only contain strings before getting used'

        try:
            # set length equal to 0
            length = 0
            for word in clean_words:
                # add length of word to length variable
                length += len(word)
            # compute average word length
            avg_wl = length / len(clean_words)

            # initialize empty list
            word_length_list = []
            for word in clean_words:
                # append length of word to the new list
                word_length_list.append(len(word))

            # create a dictionary with the frequency of each unique word in a file as well as the word count of the file
            results = {
                'wordcount': Counter(clean_words),
                'numwords': len(clean_words),
                'wordlengthlist': word_length_list,
                'avgwordlength': avg_wl
            }
        except Exception as e:
            # throw a message error if the dictionary fails to be created
            raise DataResultsError(clean_words, str(e))
        else:
            # throw a success message if the dictionary gets created
            print('Dictionary containing the word frequencies, overall word count, world length list, and average'
                  'word lengths successfully created')
            return results

    @staticmethod
    def _filter_stopwords(words):
        """ Filter out stop words from a list of given words
        Args:
            words (list): list of words that may have stop words
        Returns:
            clean_words (list): list of words that don't include the stop words
        """
        # make sure the inputted parameters are valid based on their type
        assert type(words) == list, 'Must input the words to be filtered as a list'
        for word in words:
            assert type(word) == str, 'Word list must only contain strings before getting filtered'

        try:
            # load the stop words
            stop_words = Nlp._load_stop_words()

            # make all the letters lower case and filter out the file's stop words
            # Citation: https://realpython.com/python-nltk-sentiment-analysis/
            clean_words = [word.lower() for word in words if word.lower() not in stop_words]
        except Exception as e:
            # throws an error message is the stop words cannot be filtered out
            raise StopWordError(words, str(e))
        else:
            # throws a success message if the stop words are filtered out
            print('Stop words successfully filtered out')
            return clean_words

    @staticmethod
    def _default_parser(filename):
        """ Parser that reads in a txt file

        Args:
            filename (str): name of the filename of interest
        Returns:
            results (dict): key being what kind of data gets collected about the file and value being the data itself
        """
        # Checking that the inputted parameters are valid based on their type
        assert filename[-3:] in ('csv', 'txt', 'son', 'lsx'), 'File type not supported. Only these are supported: ' \
                                                              '.csv, .txt, .json, .excel '
        assert type(filename) == str, 'File must be inputted as a string'

        try:
            # initialize empty list to store words
            words = []

            # open and read the file of interest
            text_file = open(filename, 'r')
            rows_of_text = text_file.readlines()

            # break the file into words

            # filtering the file
            for row in rows_of_text:
                # remove all break lines
                row = row.replace('\n', '')
                # remove all instances of '\u2005'
                row = row.replace('\u2005', '')
                # separate the words from each row in the txt file
                row_words = row.split(' ')

                for word in row_words:
                    # change all letters to lower case
                    word = word.lower()
                    # remove leading and trailing white-spaces
                    word = word.strip()
                    # filter out blank words and possible non-words (e.g., 'words' that start with a number)
                    if word != '' and word[0].isalpha():
                        # remove punctuation from the end of words
                        while not word[-1].isalpha():
                            word = word[:-1]
                        words.append(word)

            # close the file
            text_file.close()
        except Exception as e:
            # throws an error message if the file is not parsed
            raise DefaultParsingError(filename, str(e))
        else:
            # throws a success message if the file is successfully parsed
            print('File is successfully parsed')
            return words

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state

        Args:
            label (str): unique label for a text file that we parsed
            results (dict): the data extracted from the file as a dictionary attribute--> raw data
        """
        # Ensure the inputted parameters are valid based on their type
        assert type(label) == str, 'Label for the text file must be a string'
        assert type(results) == dict, 'The data extracted from this file must be stored in a dictionary'

        try:
            # adds the parsing results into the internal state
            for k, v in results.items():
                self.data[k][label] = v
        except Exception as e:
            # throws an error message if the results cannot be saved
            raise SaveResultsError(label, str(e))

    def load_text(self, filename, label=None, text_column='text', parser=None):
        """ Register a document with the framework

        Args:
            filename (str): name of the file of interest
            label (str): optional label for file
            parser (str): optional type of parser to be used
            text_column (str): name of column that has the text of interest
        """
        # Ensuring the inputted parameters are valid based on their type
        assert filename[-3:] in ('csv', 'txt', 'son', 'cel'), \
            'File type not supported. Only these are supported: .csv, .txt, .json, .excel'
        assert type(filename) == str, 'File must be inputted as a string'

        if label is not None:
            assert type(label) == str, 'Label for the text file must be a string'

        try:
            # do default parsing of standard .txt file
            if parser is None:
                words = Nlp._default_parser(filename)
            else:
                # checking that the custom parser is inputted as a string
                assert type(parser) == str, 'Parser must be a string'
                # do custom parsing for non- .txt files
                words = nlp_par.custom_parser(filename, text_column=text_column, parser=parser)
            # clean the list of words, removing stopwords
            clean_words = Nlp._filter_stopwords(words)
            # compute statistics/calculations regarding the list of words
            results = Nlp._data_results(clean_words)

            if label is None:
                label = filename

            # Save/integrate the data we extracted from the file into the internal state of the framework
            self._save_results(label, results)

        except Exception as e:
            # throws an error message if the document cannot be registered into the framework
            raise ParserError(filename, str(e))

        else:
            # throws a success message if the document is sucessfully registered
            print('Document is successfully registered')

    @staticmethod
    # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    def _load_stop_words(stopfile=None, parser=None):
        """ Clean the data by removing stop words

        Args:
            stopfile (str): optional txt file containing stop words, or common words that will get filtered
        Returns:
            stop_words (list): list of stopwords based on NLTK library
        """
        try:
            # retrieves a list of stopwords from the NLTK library if none is given
            if stopfile is None:
                stop_words = list(stopwords.words('english'))
            else:
                # ensure that the stop file is inputted as a string and that its file type is valid
                assert stopfile[-3:] in ('csv', 'txt', 'son', 'lsx'), \
                    'File type not supported. Only these are supported: .csv, .txt, .json, .excel'
                assert type(stopfile) == str, 'File must be inputted as a string'

                if parser is None:
                    stop_words = Nlp._default_parser(stopfile)

                else:
                    assert type(parser) == str, 'Parser must be inputted as a string'
                    # Perform parsing
                    stop_words = nlp_par.custom_parser(stopfile, text_column='text', parser=parser)
        except Exception as e:
            # throws an error message if the stop words cannot get filtered out
            raise LoadStopWordError(stopfile, str(e))
        else:
            # throws a success message if the stop words are filtered out
            print('Stop words successfully loaded')
            return stop_words

    def load_visualization(self, name, vizfunc, *args, **kwargs):
        """ Integrate visualization into internal state

        Args:
            name (str): name of visualization
            vizfunc (function): name of function to execute the visualization
            *args: unlimited number of defined parameters for the visualization
            **kwargs: unlimited number of undefined parameters for the visualization
        """
        # Ensure the inputted parameters are valid based on their type
        assert type(name) == str, 'The name of the visualization must be a string'
        assert (callable(vizfunc)), 'You must input a callable function to execute the visualization'
        try:
            # add the visualization into the internal state
            self.viz[name] = (vizfunc, args, kwargs)
        except Exception as e:
            # throws an error message if the visualization cannot get added to the internal state
            raise LoadVisualizationError(vizfunc, str(e))
        else:
            # throws a success message if the visualization is added to the internal state
            print('Visualization is successfully integrated into the internal state')

    def visualize(self, name=None):
        """ Call the vizfunc to plot the visualization

        Args:
            name (str): optional parameter for name of visualization
        """
        try:
            # run all the visualizations
            if name is None:
                for _, v in self.viz.items():
                    vizfunc, args, kwargs = v
                    vizfunc(self.data, *args, **kwargs)
            else:
                # run only the named visualization
                assert type(name) == str, 'The name of the visualization must be a string'
                vizfunc, args, kwargs = self.viz[name]
                vizfunc(self.data, *args, **kwargs)
        except Exception as e:
            # throws an error message if the visualization cannot get plotted
            raise VisualizeError(name, str(e))
        else:
            # throws a success message if the visualization gets plotted
            print('Visualization successfully plotted')
