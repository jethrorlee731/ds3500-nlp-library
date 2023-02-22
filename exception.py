"""
exception.py: ParserError class as a framework-specific exception class
"""
class ParserError(Exception):
    """ A user-defined exception for signalling parser
    error issue"""

    def __init__(self, filename, label=None, parser=None, msg=''):
        super().__init__("Wrong parser used")
        self.filename = filename
        self.label = label
        self.parser = parser


