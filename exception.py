"""
exception.py: A set of classes as  framework-specific exception classes
"""


class DataResultsError(Exception):
    """ A user-defined exception for signaling an issue with creating a dictionary containing the word frequencies,
    overall word count, world length list, and average word lengths of a file"""

    def __init__(self, clean_words):
        super().__init__("A dictionary containing the word frequencies, overall word count, world length list, and "
                         "average word lengths could not be made for this file")
        self.clean_words = clean_words


class StopWordError(Exception):
    """ A user-defined exception for signaling an issue with filtering out the stop words from a list of words"""

    def __init__(self, words):
        super().__init__("Stop words could not be filtered out")
        self.words = words


class DefaultParsingError(Exception):
    """ A user-defined exception for signaling an issue with the default parsing"""

    def __init__(self, filename):
        super().__init__("Default parsing unsuccessful")
        self.filename = filename


class SaveResultsError(Exception):
    """A user-defined exception for signaling an issue with integrating parsing results into the internal state"""

    def __init__(self, label, results):
        super().__init__("Parsing results could not be saved into the internal state")
        self.label = label
        self.results = results


class ParserError(Exception):
    """ A user-defined exception for signaling parser error issue"""

    def __init__(self, filename, label=None, parser=None):
        super().__init__("Wrong parser used")
        self.filename = filename
        self.label = label
        self.parser = parser


class LoadStopWordError(Exception):
    """ A user-defined exception for an issue with loading the stop words"""

    def __init__(self, stopfile=None, parser=None):
        super().__init__("Stop words could not be loaded")
        self.stopfile = stopfile
        self.parser = parser


class LoadVisualizationError(Exception):
    """ A user-defined exception for an issue with loading the visualization into the internal state"""

    def __init__(self, name, vizfunc):
        super().__init__("Visualization could not be integrated into the internal state")
        self.name = name
        self.vizfunc = vizfunc


class VisualizeError(Exception):
    """ A user-defined exception for an issue with plotting the visualization"""

    def __init__(self, name=None):
        super().__init__("Visualization could not be plotted")
        self.name = name
