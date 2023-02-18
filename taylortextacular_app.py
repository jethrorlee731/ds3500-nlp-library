""" BRIEF EXPLANATION OF THIS FILE """

from collections import defaultdict
from nlp import Nlp
import pprint as pp
import nlp_parsers as np
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd


def wordcount_sankey(data, word_list=None, k=5):
    """ Maps each text to words on a Sankey diagram, where the thickness of the line is the frequency of that word
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        word_list (list): a list containing a set of words to be shown on the diagram
        k (int): the union of the k most common words across each file
    Returns:
        None (just a sankey diagram!)
    """
    overall_word_count = defaultdict(lambda: 0)
    word_count_dict = data['wordcount']
    text_word_count_data = {'Text': [], 'Words': [], 'Counts': []}

    for text, word_count in word_count_dict.items():
        # Creates dictionaries with the word counts of a file. If a word list is specified, only words in that list are
        # included in the dictionary. The dictionary is sorted in descending order based on the counts.
        if word_list is None:
            word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                                reverse=True)}
        else:
            word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                                reverse=True) if word in word_list}

        # Merges the word count dictionaries of all the registered files
        text_word_count_data['Words'] += list(word_count.keys())
        text_word_count_data['Counts'] += list(word_count.values())
        text_word_count_data['Text'] += [text] * len(word_count.keys())

        # Determines the overall word counts among all the registered file. For instance, if a word appears in two
        # files, the counts of that word in both of those files are added together in a new dictionary.
        for i in range(len(text_word_count_data['Words'])):
            overall_word_count[text_word_count_data['Words'][i]] += text_word_count_data['Counts'][i]

    # Sorts the overall word counts in descending order by counts
    overall_word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                                reverse=True)}

    # if a value for k is specified, only the words with the top kth overall counts are shown on the Sankey chart
    if k is not None:
        top_words = list(overall_word_count.keys())[:k]

    # Converts the word count dictionary into a Pandas dataframe. The words are filtered based on their popularity,
    # if necessary
    df_word_counts = pd.DataFrame.from_dict(text_word_count_data)
    df_word_counts = df_word_counts[df_word_counts['Words'].isin(top_words)]

    # Makes the Sankey diagram connecting texts to words, where the thickness of a line is the number of times that word
    # occurs in the text it's linked with
    sk.make_sankey(df_word_counts, 0, 'Text', 'Words', vals=df_word_counts['Counts'])


def main():
    # initialize framework
    ts = Nlp()

    # register some text files
    ts.load_text('TaylorSwiftOurSong.txt', 'Our Song')
    ts.load_text('TaylorSwiftFearless.txt', 'Fearless')
    ts.load_text('TaylorSwiftCardigan.txt', 'Cardigan')
    ts.load_text('TaylorSwiftDearJohn.txt', 'Dear John')
    ts.load_text('TaylorSwiftGetawayCar.txt', 'Getaway Car')
    ts.load_text('TaylorSwiftLavenderHaze.txt', 'Lavender Haze')
    ts.load_text('TaylorSwiftLover.txt', 'Lover')
    ts.load_text('TaylorSwiftRed.txt', 'Red')
    ts.load_text('TaylorSwiftWelcometoNewYork.txt', 'Welcome to New York')
    ts.load_text('TaylorSwiftWillow.txt', 'Willow')

    # product sankey diagram with all 10 files
    ts.load_visualization('sankey1', wordcount_sankey)
    ts.visualize('sankey1')

    # # print out data dictionary
    # pp.pprint(ts.data)


if __name__ == '__main__':
    main()
