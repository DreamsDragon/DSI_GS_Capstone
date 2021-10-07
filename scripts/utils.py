import re
import pandas as pd
import pathlib
from pandas_profiling import ProfileReport


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

def describe_data(df,title,outpath):
    profile = ProfileReport(df, title=title,explorative = True)
    path_to_csv = pathlib.Path(outpath,"{0}.html".format(title))
    profile.to_file(path_to_csv)
