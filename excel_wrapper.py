import re
from typing import Optional, List, Any

import pandas as pd
from string import digits

excel = pd.read_csv

NAME_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y', 'Z']

OPERATOR_LIST = ['/', '*', '+', '-']
PRECEDENCE = {}
PRECEDENCE['*'] = 3
PRECEDENCE['/'] = 3
PRECEDENCE['+'] = 2
PRECEDENCE['-'] = 2
PRECEDENCE['('] = 1


def operation(data, symbol, opetaror):
    if symbol in OPERATOR_LIST:
        return float(eval("{}{}{}".format(data, symbol, opetaror)))


class Stack:
    def __init__(self):
        self.items = []
        self.length = 0

    def push(self, val):
        self.items.append(val)
        self.length += 1

    def pop(self):
        if self.empty():
            return None
        self.length -= 1
        return self.items.pop()

    def size(self):
        return self.length

    def peek(self):
        if self.empty():
            return None
        return self.items[0]

    def empty(self):
        return self.length == 0

    def __str__(self):
        return str(self.items)


def add_column_to_df(df, column_name):
    """
    This function creates a new blank column in the df
    :param df: The df to process
    :param column_name: The name of the new column
    :return: df with the added new column
    """
    # TODO check for minimum row count among all rows
    length_of_df = df.count()[0] - 1  # count of rows of first column, not the best implementation
    columns = list(df.columns)
    suffix = int(len(columns) / 26)
    if suffix:
        new_column_name = NAME_LIST[len(columns) % 26] + NAME_LIST[suffix]
    else:
        new_column_name = NAME_LIST[len(columns) % 26]
    print(pd.Series([column_name] + ([0] * 12)))
    df[new_column_name] = pd.Series([column_name] + [0] * length_of_df, index=df.index)
    return df


def pre_process_df(df):
    """
    This function pre process the df to change the look and feel of to an excel file.
    :param df: The df to processed
    :return: df, processed with headers like excel A1, B1, C1 etc.
    """
    old_columns = list(df.columns)
    new_columns = []
    # This loops create the new columns for the df, It replicates excels way on naming headers
    for i in range(len(old_columns)):
        suffix = int(i / 26)  # Calculate the numeric suffix, e.g 1 in A1
        i = i % 26
        prefix = str(NAME_LIST[i])  # Calculate the alphabetic prefix, e.g A, B etc
        if suffix != 0:
            new_columns.append(prefix + NAME_LIST[suffix])
        else:
            new_columns.append(prefix)
    df.loc[-1] = old_columns
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index
    df.columns = new_columns
    df = df.reset_index(drop=True)
    df.index += 1
    return df


def infix_to_postfix(expression):
    """
    Takes an expression and converts it to postfix notation
    :param expression: The expression to convert
    :return: list, containing postfix expression.
    """
    tokens = expression.split()
    postfix = []
    opstack = Stack()

    for token in tokens:
        if token.isidentifier() or token.isnumeric():
            postfix.append(token)
        elif token == '(':
            opstack.push(token)
        elif token == ')':
            while True:
                temp = opstack.pop()
                if temp is None or temp == '(':
                    break
                elif not temp.isidentifier():
                    postfix.append(temp)

        else:  # must be operator
            if not opstack.empty():
                temp = opstack.peek()

                while not opstack.empty() and PRECEDENCE[temp] >= PRECEDENCE[token] and token.isidentifier():
                    postfix.append(opstack.pop())
                    temp = opstack.peek()

            opstack.push(token)

    while not opstack.empty():
        postfix.append(opstack.pop())

    return postfix


def check_eval(operator_1, operator_2, symbol):
    """
    This function checks whether to apply df.eval or use apply function
    :param operator_1: operator 1
    :param operator_2: operator 1
    :param symbol: operand
    :return: str, which can be passed to df.eval or False
    """
    # strip the strings of numbers
    operator_1 = ''.join([i for i in operator_1 if not i.isdigit()])
    operator_2 = ''.join([i for i in operator_2 if not i.isdigit( )])
    if operator_1 and operator_2:
        return "{}{}{}".format(operator_2, symbol, operator_1)


def eval_postfix(df, postfix_stack, target_column):
    temp_list: List[Optional[Any]] = []
    
    print('Postfix', postfix_stack)
    for symbol in postfix_stack:
        value = None
        if symbol not in OPERATOR_LIST:
            temp_list.append(symbol)
        elif temp_list:
            operand_1, operand_2 = temp_list.pop(), temp_list.pop()
            eval_value = check_eval(operand_1, operand_2, symbol)
            print('Eval Value', eval_value)
            if eval_value:
                expression = "{}=".format(target_column) + eval_value
                columns = eval_value.split(symbol)
                for column in columns:
                    if df[column].dtype == 'object':
                        df[column] = df[column].apply(pd.to_numeric, errors='coerce')
                df = df.eval(expression, engine='python')
                temp_list.append(target_column)
            else:
                print('Not', operand_1, operand_2, symbol)
                if operand_1.isnumeric():
                    operand_2 = ''.join([i for i in operand_2 if not i.isdigit( )])
                    print(operand_2, symbol, operand_1)
                    df[operand_2] = df[operand_2].apply(operation, args=(symbol, operand_1))
                    temp_list.append(operand_2)
                    print('Done')
                else:
                    operand_1 = ''.join([i for i in operand_1 if not i.isdigit( )])
                    print(operand_1, symbol, operand_2)
                    df[operand_1] = df[operand_1].apply(operation, args=(symbol, operand_2))
                    temp_list.append(operand_1)
                    print('Done')
        # if value is not None:
        #     temp_list.append(value)
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
    first_row = df.iloc[0]
    target_column = first_row[list(df.columns).index(column)]
    print('Target Column', target_column)
    df = df[1:]
    print(function)
    expression = function.split('=')[1]
    postfix_expression = infix_to_postfix(expression)
    df = eval_postfix(df, postfix_expression, column)
    print('expression to solve', postfix_expression)
    df.loc[-1] = first_row
    df.index = df.index + 1  # shifting index
    df = df.sort_index( )  # sorting by index
    df = df.reset_index(drop=True)
    df.index += 1
    df['id'] = range(1, len(df) + 1)
    return df.to_html()


df = pd.read_csv(
    "/home/neel/Work/Office/test_files/Clean Data-20180522T112152Z-001/Clean Data/Nakul/Date in row/OpenClaims.csv",
    error_bad_lines=False
)

df = pre_process_df(df)
df = add_column_to_df(df, column_name='Profit')
processed_df = excel_functions(
    df=df,
    function='=( ( ( G2 - H2 ) / G2 ) * 100 )',
    column="I",
    row=None
)
html_file = open("demo_html.html", "w")
html_file.write(processed_df)
html_file.close()
