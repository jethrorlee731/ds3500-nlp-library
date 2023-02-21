""" BRIEF EXPLANATION OF THIS FILE """

from collections import defaultdict
from nlp import Nlp
import pprint as pp
import nlp_parsers as np
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd
from exception import ParserError
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def wordcount_sankey(data, word_list=None, k=5):
    """ Maps each text to words on a Sankey diagram, where the thickness of the line is the frequency of that word
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        word_list (list): a list containing a set of words to be shown on the diagram
        k (int): the union of the k most common words across each file
    Returns:
        None (just a sankey diagram!)
    """
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'
    assert type(k) == int, 'The number of words considered from each file for analysis must be an integer'

    if word_list is not None:
        assert type(word_list) == list, 'Must input the words to be shown on the diagram as a list'
        assert type(all(word for word in word_list)) == str, 'Word list must only contain strings'

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
    overall_word_count = {word: count for word, count in sorted(overall_word_count.items(), key=lambda item: item[1],
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


def sentiment_analysis_bars(data, subplot_rows=5, subplot_columns=2, k=None):
    # Citation: https://realpython.com/python-nltk-sentiment-analysis/
    """ Creates a bar chart for each file representing their overall sentiments
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        subplot_rows (int): the number of rows in the sub-plot
        subplot_columns (int): the number of columns in the sub-plot
        k (int): the number of words considered from each file for analysis, based on their frequencies
    Returns:
        None (just bar charts!)
    """
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'
    assert type(subplot_rows) == int, 'The number of rows for the subplot must be an integer'
    assert type(subplot_columns) == int, 'The number of columns for the subplot must be an integer'

    texts = []
    sentiment_distributions = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize a sentiment intensity analyzer
    sia = SentimentIntensityAnalyzer()

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = ''
        # if a k value is given, restrict the analysis to consider only the k most popular words in each file
        if k is not None:
            assert type(k) == int, 'The number of words considered from each file for analysis must be an integer'
            word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                                reverse=True)}
            word_count = dict(word_count.items()[:k])
        for word, count in word_count.items():
            word = (word + ' ') * count
            words += word

        # calculate the sentiment distributions (negative vs. neutral vs. positive) for each file and store them in a
        # dictionary
        sentiment_distribution = sia.polarity_scores(words)

        # store the names of the files as well as its sentiment distribution dictionaries
        texts.append(text)
        sentiment_distributions.append(sentiment_distribution)

    # Creates subplots showing the sentiment score distributions (positive vs. neutral vs. negative) of each file as
    # bar charts
    for i in range(len(texts)):
        plt.subplot(subplot_rows, subplot_columns, i + 1)
        for sentiment, score in sentiment_distributions[i].items():
            # displays the negative score of a text file
            if sentiment == 'neg':
                plt.barh('Negative', score, label='Negative', color='firebrick')
            # displays the neutral score of a text file
            elif sentiment == 'neu':
                plt.barh('Neutral', score, label='Neutral', color='gold')
            # displays the positive score of a text file
            elif sentiment == 'pos':
                plt.barh('Positive', score, label='Positive', color='limegreen')

            # Each subplot is labeled based on the text they are representing
            plt.gca().title.set_text('Sentiment Distributions For "' + texts[i] + '"')

    # Gives the plot a title
    plt.suptitle('Overall Sentiment Distributions')

    # resizes the graph to ensure that it can be clearly read
    plt.gcf().set_size_inches(50, 14)

    # adjusts spacing between graphs
    plt.subplots_adjust(wspace=.8, hspace=.8)

    # display the bar charts
    plt.show()

def avgwlength_boxplot(data):
    """ Creates a boxplot of word lengths on one visualization with labels for each of the files, showing distributions
    Citation:
    https://www.tutorialspoint.com/creating-multiple-boxplots-on-the-same-graph-from-a-dictionary-using-matplotlib

    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (boxplot in one visualization of all the files)
    """
    # obtain the word length dictionary
    word_length_dict = data['wordlengthlist']

    # set the figure size
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # create a figure with the subplots
    fig, ax = plt.subplots()

    # plot the boxplot with labels
    ax.boxplot(word_length_dict.values())
    ax.set_xticklabels(word_length_dict.keys(), rotation=90, fontsize=5)

    # make the boxplot show
    plt.show()

def avgwlength_bar(data):
    """ Creates a bar chart of the average word length for each of the files
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just a bar chart)
    """
    # obtain the avg word length dictionary
    avg_wordl_dict = data['avgwordlength']

    # get the labels and values in separate variables
    label = list(avg_wordl_dict.keys())
    value = list(avg_wordl_dict.values())

    # set the figure size
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # plot the bar chart, style the x ticks, label the axes and title
    plt.bar(range(len(avg_wordl_dict)), value, tick_label=label)
    plt.xticks(rotation=90, fontsize=5)
    plt.xlabel('Name of Song')
    plt.ylabel('Average Word Length')
    plt.title('Average Word Lengths for the Different Songs')

    # make the chart show
    plt.show()

def total_wordl_boxplot(data):
    """ Create a boxplot that gives distribution of the word length for all the files combined
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just a boxplot)
    """
    # obtain the word length list dictionary
    word_length_dict = data['wordlengthlist']

    # get just the word lengths
    total_wl_list = list(word_length_dict.values())

    # turn the 2d list into 1d
    total_wl_list = [item for sublist in total_wl_list for item in sublist]

    # set the figure size
    fig = plt.figure(figsize=(10, 7))

    # create the box plot, set the axes and title
    plt.boxplot(total_wl_list)
    plt.ylabel("Word Length")
    plt.title("Word Length Distribution for All Files Combined")

    # show plot
    plt.show()


def main():
    # download a package needed for sentiment analysis
    nltk.download('vader_lexicon')

    # initialize framework
    ts = Nlp()

    try:
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
    except ParserError as pe:
        print(str(pe))

    # produce sankey diagram with the passed in files
    ts.load_visualization('sankey1', wordcount_sankey)
    ts.visualize('sankey1')

    # produce sentiment analysis bar charts for each of the files passed in
    ts.load_visualization('sentiment1', sentiment_analysis_bars, 5, 2)
    ts.visualize('sentiment1')

    # produce boxplot about length of words for each of the files passed in
    ts.load_visualization('boxplot1', avgwlength_boxplot)
    ts.visualize('boxplot1')

    # produce bar chart for average length of words
    ts.load_visualization('barchart1', avgwlength_bar)
    ts.visualize('barchart1')

    # produce a box plot for length of words for all the files combined
    ts.load_visualization('totalboxplot1', total_wordl_boxplot)
    ts.visualize('totalboxplot1')

    # print out data dictionary
    pp.pprint(ts.data)


if __name__ == '__main__':
    main()
