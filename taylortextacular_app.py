""" BRIEF EXPLANATION OF THIS FILE """

from nlp import Nlp
import pprint as pp
import nlp_parsers as np
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd

def wordcount_sankey(data, word_list=None, k=5):
    """ Maps each text to words on a Sankey diagram, where the thickness of the line is the frequency of that word
    Args:
        word_list (list): a list containing a set of words to be shown on the diagram
        k (int): the union of the k most common words across each file
    Returns:
        None (just a sankey diagram!)
    """
    word_count_dict = data['wordcount']

    texts = []
    all_words = []
    all_counts = []

    for text, word_count in word_count_dict.items():
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}
        words = list(word_count.keys())
        if word_list is None:
            if k is not None:
                words = words[:k + 1]
        else:
            words = [word for word in words if word in word_list]
        counts = list(word_count.values())
        counts = counts[:k + 1]
        text = [text] * len(words)

        texts += text
        all_words += words
        all_counts += counts

    word_count = list(zip(all_words, all_counts, texts))
    df_word_counts = pd.DataFrame(word_count, columns=['Word', 'Counts', 'Text'])
    # print(df_word_counts)
    sk.make_sankey(df_word_counts, 0, 'Text', 'Word', vals=df_word_counts['Counts'])


def main():
    # initialize framework
    ts = Nlp()

    # register some text files
    ts.load_text('TaylorSwiftOurSong.txt', 'Our Song')
    ts.load_text('TaylorSwiftFearless.txt', 'Fearless')
    # ts.load_text('TaylorSwiftCardigan.txt', 'Cardigan')
    # ts.load_text('TaylorSwiftDearJohn.txt', 'Dear John')
    # ts.load_text('TaylorSwiftGetawayCar.txt', 'Getaway Car')
    # ts.load_text('TaylorSwiftLavenderHaze.txt', 'Lavender Haze')
    # ts.load_text('TaylorSwiftLover.txt', 'Lover')
    # ts.load_text('TaylorSwiftRed.txt', 'Red')
    # ts.load_text('TaylorSwiftWelcometoNewYork.txt', 'Welcome to New York')
    # ts.load_text('TaylorSwiftWillow.txt', 'Willow')

    # product sankey diagram with all 10 files
    ts.load_visualization('sankey1', wordcount_sankey)
    ts.visualize('sankey1')

    # # print out data dictionary
    # pp.pprint(ts.data)


if __name__ == '__main__':
    main()
