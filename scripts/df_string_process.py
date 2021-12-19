import re
import pandas as pd

def process_columns(df, columns):
    """Function for preprocessing string columns in pandas dataframe

    Args:
        df (pandas dataframe): pandas dataframe to be preprocessed
        columns (list): list of string columns to be preprocessed

    Returns:
        pandas dataframe: preprocessed dataframe
    """
    for column in columns:
        df[column] = df[column].str.upper().str.strip().str.replace('\W+', '')
    return df
