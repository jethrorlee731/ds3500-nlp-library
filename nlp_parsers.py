"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

nlp_parsers.py: json, csv, and excel parsers to get the interested column from the files
"""
# import necessary libraries
import pandas as pd


def custom_parser(filename, text_column, parser):
    """ Take the pandas dataframe of the file read in and return a list of only the interested words
    Args:
        filename (str): name of interested json filename
        text_column (str): name of interested column from the dataframe
        parser (str): type of custom parser to be used (json, csv, or excel)
    Returns:
        clean_words_list (list) list of words (str) of the interested words from the file
    """
    # initialize empty list
    clean_words_list = []

    # read in json file into a dataframe
    if parser == 'json':
        df = pd.read_json(filename)

    # read in csv file into a dataframe
    elif parser == 'csv':
        df = pd.read_csv(filename)

    # read in csv file into a dataframe
    else:
        df = pd.read_excel(filename)

    # get the interested column that has texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    for word in words_list:
        # remove leading and trailing white-spaces
        word = word.strip()
        clean_words_list.append(word)

    return clean_words_list
