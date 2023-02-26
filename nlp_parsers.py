"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

nlp_parsers.py: JSON, CSV, and Excel parsers to get the store the text contents of a file into a list of its words
"""
# import necessary libraries
import pandas as pd


def custom_parser(filename, text_column, parser):
    """ Reads in a file to make a Pandas dataframe out of and returns a list of only the words of interest
    Args:
        filename (str): name of the file of interest
        text_column (str): name of column of interest from the dataframe (which contains the texts)
        parser (str): type of custom parser to be used (json, csv, or Excel)
    Returns:
        clean_words_list (list): list of words (str) of the interested words from the file
    """
    assert type(filename) == str, 'File name must be specified as a string'
    assert type(text_column) == str, 'The column of the new dataframe which contains the texts must be specified as ' \
                                     'a string'
    assert parser in ('json', 'csv', 'excel'), 'Unsupported file type'

    # initialize empty list
    clean_words_list = []

    # read in JSON file into a dataframe
    if parser == 'json':
        df = pd.read_json(filename)

    # read in CSV file into a dataframe
    elif parser == 'csv':
        df = pd.read_csv(filename)

    # read in Excel file into a dataframe
    else:
        df = pd.read_excel(filename)

    # get the column that has the texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    for word in words_list:
        # remove leading and trailing white-spaces
        word = word.strip()
        clean_words_list.append(word)

    return clean_words_list
