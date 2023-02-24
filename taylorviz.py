"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

taylorviz.py: different visualizations to be made
"""
# import necessary libraries
from collections import defaultdict
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud


def convert_file_to_string(word_count, max_words=None):
    """ Extracts the words from a file and compiles them into one sting
    Args:
        word_count (dict): contains the words in a file (key) and their frequencies (value)
        max_words (int): the number of words considered from each file for analysis, based on their frequencies
    """
    words = ''
    # if max_words is given, restrict the analysis to consider only the max_words number of
    # most popular words in each file
    if max_words is not None:
        assert type(max_words) == int, 'The number of words considered from each file for analysis must be an integer'
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}
        word_count = dict(word_count.items()[:max_words])
    for word, count in word_count.items():
        # Extract each word in the word count dictionary and repeat them in the returned string based on their
        # frequency in the file
        word = (word + ' ') * count
        words += word

    # return the string
    return words


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
        assert all(isinstance(word, str) for word in word_list), 'Word list must only contain strings'

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize empty lists
    texts = []
    all_words = []
    all_counts = []

    for text, word_count in word_count_dict.items():
        # Sorts the word counts in descending order by counts
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}
        # get a list of only the keys
        words = list(word_count.keys())

        if k is not None:
            # get only the top k words
            for word in words[:k]:
                if word_list is None or len(word_list) == 0:
                    word_list = []
                if word not in word_list:
                    word_list.append(word)

    for text, word_count in word_count_dict.items():
        # Sorts the word counts in descending order by counts
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}

        for word, count in word_count.items():
            if word in word_list:
                all_words.append(word)
                all_counts.append(count)
                texts += [text]

    word_count = list(zip(all_words, all_counts, texts))
    df_word_counts = pd.DataFrame(word_count, columns=['Word', 'Counts', 'Text'])
    sk.make_sankey(df_word_counts, 0, 'Text', 'Word', vals=df_word_counts['Counts'])


def sentiment_analysis_bars(data, subplot_rows=5, subplot_columns=2, max_words=None):
    # Citation: https://realpython.com/python-nltk-sentiment-analysis/
    """ Creates a bar chart for each file representing their overall sentiments
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        subplot_rows (int): the number of rows in the sub-plot
        subplot_columns (int): the number of columns in the sub-plot
        max_words (int): the number of words considered from each file for analysis, based on their frequencies
    Returns:
        None (just bar charts!)
    """
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'
    assert type(subplot_rows) == int, 'The number of rows for the subplot must be an integer'
    assert type(subplot_columns) == int, 'The number of columns for the subplot must be an integer'

    # initialize empty lists
    texts = []
    sentiment_distributions = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize a sentiment intensity analyzer
    sia = SentimentIntensityAnalyzer()

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)
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


def sentiment_scatter(data, max_words=None):
    """ Scatter plot with the x being the count of positive words and y being the count of negative words
    Each point is a file.

    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        max_words (int): the number of words considered from each file for analysis, based on their frequencies
    Returns:
        none (just a scatter plot)
    """
    # initialize empty lists
    texts = []
    positive_distributions = []
    negative_distributions = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize a sentiment intensity analyzer
    sia = SentimentIntensityAnalyzer()

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)
        # calculate the sentiment distributions (negative vs. neutral vs. positive) for each file and store them in a
        # dictionary
        sentiment_distribution = sia.polarity_scores(words)
        pos_score = sentiment_distribution['pos']
        neg_score = sentiment_distribution['neg']
        # store the names of the files as well as its sentiment distribution dictionaries
        texts.append(text)
        positive_distributions.append(pos_score)
        negative_distributions.append(neg_score)

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(positive_distributions, negative_distributions)

    for i, txt in enumerate(texts):
        ax.annotate(txt, (positive_distributions[i], negative_distributions[i]))

    plt.xlabel('Positive Score')
    plt.ylabel('Negative Score')
    plt.title('Negative vs Positive Score of Different Songs')
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
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'

    # obtain the word length dictionary
    word_length_dict = data['wordlengthlist']

    # set the figure size
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True

    # create a figure with the subplots
    fig, ax = plt.subplots()

    # plot the boxplot with labels
    ax.boxplot(word_length_dict.values())
    ax.set_xticklabels(word_length_dict.keys(), rotation=90, fontsize=5)
    plt.xlabel('Name of Song')
    plt.ylabel('Average Word Length Distributions')
    plt.title('Average Word Length Distributions for the Different Songs')

    # make the boxplot show
    plt.show()


def avgwlength_bar(data):
    """ Creates a bar chart of the average word length for each of the files
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just a bar chart)
    """
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'

    # obtain the avg word length dictionary
    avg_wordl_dict = data['avgwordlength']

    # get the labels and values in separate variables
    label = list(avg_wordl_dict.keys())
    value = list(avg_wordl_dict.values())

    # set the figure size
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True

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
    # Exception handling for the given parameters
    assert type(data) == defaultdict, 'The data extracted from this file must be stored in a dictionary'

    # obtain the word length list dictionary
    word_length_dict = data['wordlengthlist']

    # get just the word lengths
    total_wl_list = list(word_length_dict.values())

    # turn the 2d list into 1d
    total_wl_list = [item for sublist in total_wl_list for item in sublist]

    # set the figure size
    plt.figure(figsize=(10, 7))

    # create the box plot, set the axes and title
    plt.boxplot(total_wl_list)
    plt.ylabel('Word Length')
    plt.title('Word Length Distribution for All Files Combined')

    # show plot
    plt.show()


def make_wordclouds(data, colormaps=None, background_color='black', min_font_size=4, normalize_plurals=True,
                    collocations=False, subplot_rows=4, subplot_columns=3, max_words=None):
    """ Creates a word cloud that shows the words in a text, with words that appear more frequently appearing larger
        Args:
            data (dict): data extracted from the file as a dictionary attribute--> raw data
            colormaps (list of strings): List of color schemes for the words on the diagram
            background_color (string): the color of the word cloud's background
            min_font_size (int): The minimum font size used on the words
            normalize_plurals (boolean): A boolean value indicating whether the trailing 's' in words should be removed
            collocations (boolean): A boolean value indicating whether bigrams are considered
            subplot_rows (int): the number of rows in the sub-plot
            subplot_columns (int): the number of columns in the sub-plot
            max_words (int): The maximum number of words represented on the word cloud
        Returns:
            None (just word clouds)
        """
    # Assertion statements for input parameters
    if colormaps is not None:
        assert type(colormaps) == list, 'The color schemes of the wordcloud must be entered in a list'
        for colormap in colormaps:
            assert type(colormap) == str, 'The colormaps for each word cloud must be entered as strings'
    assert type(background_color) == str, 'The background color of the wordcloud must be entered as a string'
    assert type(min_font_size) == int, 'The minimum font size of the wordcloud must be entered as an integer'
    assert type(normalize_plurals) == bool, 'You must indicate whether the plural form of a word should be considered' \
                                            'the same as its singular form with "True" or "False"'
    assert type(collocations) == bool, 'You must indicate whether bigrams are considered with "True" or "False"'
    assert type(subplot_rows) == int, 'The number of rows for the subplot must be an integer'
    assert type(subplot_columns) == int, 'The number of columns for the subplot must be an integer'

    # initialize empty lists
    texts = []
    word_strings = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)

        texts.append(text)
        word_strings.append(words)

    # generates the word cloud figure
    plt.figure()

    # defines the default colormap
    if colormaps is None:
        colormaps = ['viridis'] * len(texts)

    for i in range(len(texts)):
        # generate a subplot word cloud for each file
        plt.subplot(subplot_rows, subplot_columns, i + 1)
        wordcloud = WordCloud(background_color=background_color, colormap=colormaps[i], min_font_size=min_font_size,
                              normalize_plurals=normalize_plurals, collocations=collocations).generate(word_strings[i])

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        # Each subplot is labeled based on the text they are representing
        plt.gca().title.set_text('Word Cloud For "' + texts[i] + '"')

    # Gives the plot a title
    plt.suptitle('Overall Word Counts')

    # resizes the graph to ensure that it can be clearly read
    plt.gcf().set_size_inches(50, 14)

    # adjusts spacing between graphs
    plt.subplots_adjust(wspace=.8, hspace=.8)

    # presents the word clouds
    plt.show()
