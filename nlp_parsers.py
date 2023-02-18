""" BRIEF EXPLANATION OF THIS FILE """
import json
from collections import Counter


def json_parser(filename, text_column):
    words_list = []
    f = open(filename, 'r')
    raw = json.load(f)
    for item in raw:
        words = item[text_column].split()
        for word in words:
            words_list.append(word)
    f.close()
    return words_list
