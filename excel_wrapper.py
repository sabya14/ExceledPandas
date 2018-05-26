import re

import pandas as pd
import numpy as np
from string import digits

excel = pd.read_csv


def add_column_to_df(df, column_name):
    """
    This function creates a new blank column in the df
    :param df: The df to process
    :param column_name: The name of the new column
    :return: df with the added new column
    """
    # TODO check for minimum row count among all rows
    length_of_df = df.count()[0] + 2  # count of rows of first column, not the best implementation
    df[column_name] = pd.Series([0] * length_of_df)
    return df


def pre_process_df(df):
    """
    This function pre process the df to change the look and feel of to an excel file.
    :param df: The df to processed
    :return: df, processed with headers like excel A1, B1, C1 etc.
    """
    old_columns = list(df.columns)
    name_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
    new_columns = []
    # This loops create the new columns for the df, It replicates excels way on naming headers
    for i in range(len(old_columns)):
        suffix = int(i / 26)  # Calculate the numeric suffix, e.g 1 in A1
        i = i % 26
        prefix = str(name_list[i])  # Calculate the alphabetic prefix, e.g A, B etc
        if suffix != 0:
            new_columns.append(prefix + name_list[suffix])
        else:
            new_columns.append(prefix)
    df.loc[-1] = old_columns
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index
    df.columns = new_columns
    df = df.reset_index(drop=True)
    df.index += 1
    return df


def excel_functions(df, function, column, row=None):
    """
    The main motive of this wrapper is to evaluate an excel function(Recieved as string from user) and map it into an pandas
    function. Then make the changes real time in the data frame and return it to user.

    :param df: The df to process
    :param function: The function passed by user
    :param column: The column to understand where to operate
    :param row: In addition with column get the row number to figure exact cell for the operation, of none understand
                that operations is for whole row, else cell specific
    :return: data frame, processed df
    """
    opertors_operands_list = re.split('(\W+)', function)
    opertors_operands_list.remove('')
    if '=' in opertors_operands_list:
        opertors_operands_list.remove("=")
    for index, elements in enumerate(opertors_operands_list):
        if elements.isalnum():
            remove_digits = str.maketrans('', '', digits)
            elements = elements.translate(remove_digits)
            opertors_operands_list[index] = elements

    print("{}=".format(column) + "".join(opertors_operands_list))
    expr = "{}=".format(column) + "".join(opertors_operands_list)
    df.eval(expr, inplace=True)
    return df.to_html()


df = pd.read_csv(
    "/home/neel/Work/Office/test_files/Clean Data-20180522T112152Z-001/Clean Data/Nakul/Date in row/OpenClaims.csv",
    error_bad_lines=False
)

df = pre_process_df(df)
df = add_column_to_df(df, column_name='Total')
processed_df = excel_functions(
    df=df,
    function='=A2+B2',
    column="Total",
    row=None
)
html_file = open("demo_html.html", "w")
html_file.write(processed_df)
html_file.close()
