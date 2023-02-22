"""
nlp_parsers.py: json, csv, and excel parsers to get the interested column from the files
"""
import pandas as pd

def json_parser(filename, text_column):
    """ Read in a json file and turn the words in the text_column into a 1d list
    Args:
        filename (str): name of interested json filename
        text_column (str): name of interested column from the file

    Returns:
        words_list (list): list of words (str) from the file
    """
    # read in json file into a dataframe
    df = pd.read_json(filename)

    # get the interested column that has texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    return words_list


def csv_parser(filename, text_column):
    """ Read in a csv file and turn the words in the text_column into a 1d list
    Args:
        filename (str): name of interested csv filename
        text_column (str): name of interested column from the file

    Returns:
        words_list (list): list of words (str) from the file
    """
    # read in csv file into a dataframe
    df = pd.read_csv(filename)

    # get the interested column that has texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    return words_list

def excel_parser(filename, text_column):
    """ Read in an excel file and turn the words in the text_column into a 1d list
    Args:
        filename (str): name of interested csv filename
        text_column (str): name of interested column from the file
    Returns:
        words_list (list): list of words (str) from the file
    """
    # read in csv file into a dataframe
    df = pd.read_excel(filename)

    # get the interested column that has texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    return words_list
