"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

taylortextacular_app.py: main file for loading the files as well as loading the visualizations specified by specific
user-defined functions from the visualization library (taylorviz)
"""

# import necessary libraries
from nlp import Nlp
from exception import LoadStopWordError
import nltk
import taylorviz as tviz


def main():
    # download a package needed for sentiment analysis
    nltk.download('vader_lexicon')

    # download a package needed for removing the stop words from a file
    nltk.download('stopwords')

    # initialize framework
    ts = Nlp()

    # create a list of the files getting registered and a list of their labels
    files = ['TaylorSwiftOurSong.txt', 'TaylorSwiftFearless.txt', 'TaylorSwiftDearJohn.txt', 'TaylorSwiftRed.txt',
             'TaylorSwiftWelcometoNewYork.txt', 'TaylorSwiftGetawayCar.txt', 'TaylorSwiftLover.txt',
             'TaylorSwiftCardigan.txt', 'TaylorSwiftWillow.txt', 'TaylorSwiftLavenderHaze.txt']
    file_labels = ['Our Song', 'Fearless', 'Dear John', 'Red', 'Welcome to New York', 'Getaway Car', 'Lover',
                   'Cardigan', 'Willow', 'Lavender Haze']

    try:
        # register some text files
        for i in range(len(files)):
            ts.load_text(files[i], file_labels[i])

    except LoadStopWordError as pe:
        # indicates whether there was an issue with registering the files
        print(str(pe))

    # produce a Sankey diagram linking the top 5 words within each registered file to the files they are present in
    ts.load_visualization('sankey', tviz.wordcount_sankey)
    ts.visualize('sankey')

    # produce a wordcloud for the word counts from each file

    # colors used for the word cloud
    word_cloud_colors = ['summer', 'Wistia', 'BuPu', 'Reds', 'Blues', 'bone', 'spring_r', 'gist_yarg', 'copper',
                         'Purples']

    ts.load_visualization('wordcloud', tviz.make_word_clouds, colormaps=word_cloud_colors)
    ts.visualize('wordcloud')

    # produce a scatter plot showing the relationship between the degree to which a file's tone is positive vs. negative
    ts.load_visualization('sentimentscatter', tviz.sentiment_scatter)
    ts.visualize('sentimentscatter')

    # produce sentiment analysis bar subplots (positive vs. neutral vs. negative scores) for each of the files passed in
    ts.load_visualization('sentimentbar', tviz.sentiment_analysis_bars, 5, 2)
    ts.visualize('sentimentbar')

    # produce a boxplot summarizing the lengths of the words in each of the files passed in
    ts.load_visualization('boxplot', tviz.avgwlength_boxplot)
    ts.visualize('boxplot')

    # produce a bar chart comparing the average length of the words in each registered file
    ts.load_visualization('barchart', tviz.avgwlength_bar)
    ts.visualize('barchart')

    # produce a box plot summarizing the lengths of the words in all the files combined
    ts.load_visualization('totalboxplot', tviz.total_wordl_boxplot)
    ts.visualize('totalboxplot')


if __name__ == '__main__':
    main()
