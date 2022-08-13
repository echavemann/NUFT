import pandas as pd
import csv

def csv_reader(start_seconds, end_seconds):
    file = str('RAW_DATA_' + start_seconds + 'to' + end_seconds + '_.csv')
    df = pd.read_csv(file)
    return df

def csv_reader_path(file_path):
    """
    Reads a csv file and returns a pandas dataframe
    """
    df = pd.read_csv(file_path)
    return df

def csv_writer(file_path, df):
    """
    Writes a pandas dataframe to a csv file
    """
    df.to_csv(file_path, index=False)
    return None

def csv_writer_append(file_path, df):
    """
    Appends a pandas dataframe to a csv file
    """
    df.to_csv(file_path, mode='a', header=False, index=False)
    return None

def csv_writer_append_header(file_path, df):
    """
    Appends a pandas dataframe to a csv file with a header
    """
    df.to_csv(file_path, mode='a', header=True, index=False)
    return None

def pd_sorting(df, ascend, column_name):
    """
    Sorts a pandas dataframe by a column
    """
    df.sort_values(by=column_name, ascending=ascend, inplace=True)
    return df
