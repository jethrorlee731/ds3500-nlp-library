""" BRIEF EXPLANATION OF THIS FILE """
import json
from collections import Counter


def json_parser(filename):
    f = open(filename, 'r')
    raw = json.load(f)
    text = raw['text']
    words = text.split(' ')
    wc = Counter(words)
    num = len(words)
    f.close()

    return {'wordcount': wc, 'numwords': num}
