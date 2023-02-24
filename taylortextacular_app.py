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

    # download a package needed for stopwords
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
        print(str(pe))

    # produce sankey diagram with the passed in files
    ts.load_visualization('sankey1', tviz.wordcount_sankey)
    ts.visualize('sankey1')

    # produce sentiment analysis bar charts for each of the files passed in
    ts.load_visualization('sentiment1', tviz.sentiment_analysis_bars, 5, 2)
    ts.visualize('sentiment1')

    # produce boxplot about length of words for each of the files passed in
    ts.load_visualization('boxplot1', tviz.avgwlength_boxplot)
    ts.visualize('boxplot1')

    # produce bar chart for average length of words
    ts.load_visualization('barchart1', tviz.avgwlength_bar)
    ts.visualize('barchart1')

    # produce a box plot for length of words for all the files combined
    ts.load_visualization('totalboxplot1', tviz.total_wordl_boxplot)
    ts.visualize('totalboxplot1')

    # produce a wordcloud for word counts from each file
    # colors used for the word cloud
    wordcloud_colors = ['summer', 'Wistia', 'BuPu', 'Reds', 'Blues', 'bone', 'spring_r', 'gist_yarg', 'copper',
                        'Purples']
    ts.load_visualization('wordcloud1', tviz.make_wordclouds, colormaps=wordcloud_colors)
    ts.visualize('wordcloud1')

    # produce a scatter plot with the count of positive words and being of negative words
    ts.load_visualization('sentimentscatter', tviz.sentiment_scatter)
    ts.visualize('sentimentscatter')


if __name__ == '__main__':
    main()
