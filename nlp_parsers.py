""" BRIEF EXPLANATION OF THIS FILE """
import json
import csv
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


def csv_parser(filename):
    # SHOULD BE TESTED
    words_list = []
    with open(filename, 'r') as f:
        rows = csv.reader(f)
        for row in rows:
            row_as_string = ''.join(row)
            words = row_as_string.split(',')
            words_list.append(words)
    f.close()
    return words_list
