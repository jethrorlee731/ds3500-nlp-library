"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

taylortextacular_app.py: main file to run the nlp loading of dataset as well as loading of visualizations specified
by specific user-defined functions from the visualization file
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

    try:
        # register some text files
        ts.load_text('TaylorSwiftOurSong.txt', 'Our Song')
        ts.load_text('TaylorSwiftFearless.txt', 'Fearless')
        ts.load_text('TaylorSwiftDearJohn.txt', 'Dear John')
        ts.load_text('TaylorSwiftRed.txt', 'Red')
        ts.load_text('TaylorSwiftWelcometoNewYork.txt', 'Welcome to New York')
        ts.load_text('TaylorSwiftGetawayCar.txt', 'Getaway Car')
        ts.load_text('TaylorSwiftLover.txt', 'Lover')
        ts.load_text('TaylorSwiftCardigan.txt', 'Cardigan')
        ts.load_text('TaylorSwiftWillow.txt', 'Willow')
        ts.load_text('TaylorSwiftLavenderHaze.txt', 'Lavender Haze')

    except LoadStopWordError as pe:
        # indicates whether there was an issue with registering the files
        print(str(pe))

    # produce a Sankey diagram for the top 5 words within each registered file
    ts.load_visualization('sankey', tviz.wordcount_sankey)
    ts.visualize('sankey')

    # produce a wordcloud for the word counts from each file

    # colors used for the word cloud
    wordcloud_colors = ['summer', 'Wistia', 'BuPu', 'Reds', 'Blues', 'bone', 'spring_r', 'gist_yarg', 'copper',
                        'Purples']

    ts.load_visualization('wordcloud', tviz.make_wordclouds, colormaps=wordcloud_colors)
    ts.visualize('wordcloud')

    # produce a scatter plot showing the relationship between the degree to which a file's tone is positive vs. negative
    ts.load_visualization('sentimentscatter', tviz.sentiment_scatter)
    ts.visualize('sentimentscatter')

    # produce sentiment analysis bar subplots for each of the files passed in
    ts.load_visualization('sentimentbar', tviz.sentiment_analysis_bars, 5, 2)
    ts.visualize('sentimentbar')

    # produce a boxplot about the lengths of the words for each of the files passed in
    ts.load_visualization('boxplot', tviz.avgwlength_boxplot)
    ts.visualize('boxplot')

    # produce a bar chart for average length of the words in each registered file
    ts.load_visualization('barchart', tviz.avgwlength_bar)
    ts.visualize('barchart')

    # produce a box plot summarizing the length of the words for all the files combined
    ts.load_visualization('totalboxplot', tviz.total_wordl_boxplot)
    ts.visualize('totalboxplot')


if __name__ == '__main__':
    main()
