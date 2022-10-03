# import xlrd, xlwings
from collections import namedtuple

from colorama import Fore, Style, Back
import os.path
import math
import pandas as pd
import numpy as np
import main
from datetime import date
from warnings import filterwarnings
import datetime
import time
import builtins
import traceback
import sys

filterwarnings('ignore', category=UserWarning, module='openpyxl')



def check_files_list(folder_path):

    extensions = ['.xlsx', '.xls', '.xlsm', '.xlsb']
    wrong = ['~$']
    correct_list = []

    file_list = [file for file in os.listdir(folder_path)
                 if not os.path.isdir(os.path.join(folder_path, file))]
    file_list_lower = [file.lower() for file in file_list]

    for file_lower, file in zip(file_list_lower, file_list):
        for ext in extensions:
            for wr in wrong:
                if ext in file_lower and wr not in file_lower:
                    correct_list.append(file)

    return set(correct_list)

def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        func(*args, **kwargs)
        end = datetime.datetime.now()
        print()
        print('Process takes - ', end - start, ' sec', sep='')

    return wrapper

def find_children(file_path):
    parent_dict = dict()
    parent_name = os.path.basename(os.path.normpath(file_path))
    parent_dict[parent_name] = list()
    children = os.listdir(file_path)

    for child in children:

        if os.path.isdir(os.path.join(file_path, child)):
            child_path = os.path.join(file_path, child)
            child_hierarchy = find_children(child_path)
            parent_dict[parent_name].append(child_hierarchy)
        else:
            parent_dict[parent_name].append(child)

    return parent_dict


def get_file_size(file_path):
    bytes_in_megabyte = 1024 * 1024
    size = os.path.getsize(file_path) / bytes_in_megabyte

    return size


def get_create_date(file_path):
    # s1 = path.getctime(file_path)
    s1 = os.stat(file_path).st_birthtime
    s2 = datetime.datetime.strptime(time.ctime(s1), '%c').date()
    s3 = s2.strftime('%d/%m/%Y')

    return s3


def get_mod_date(file_path):
    s1 = os.path.getmtime(file_path)
    s2 = datetime.datetime.strptime(time.ctime(s1), '%c').date()
    s3 = s2.strftime('%d/%m/%Y')

    return s3


def tmp(df: pd.DataFrame):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def add_extracting_time_info(df: pd.DataFrame):
    extract_timestamp = datetime.datetime.now()

    df['extracting_date'] = extract_timestamp.strftime('%d.%m.%Y')
    df['extracting_time'] = extract_timestamp.strftime('%H:%M')

    return df


def add_edit_time_info(df: pd.DataFrame, fem_folder, filename):
    edit_timestamp = os.path.getmtime(os.path.join(fem_folder, filename))
    datestamp = datetime.datetime.fromtimestamp(edit_timestamp)

    df['edit_date'] = datestamp.strftime('%d.%m.%Y')
    df['edit_time'] = datestamp.strftime('%H:%M')

    return df

def check_duplicate_column_name(df: pd.DataFrame):
    duplicates = [column_name for column_name in df.columns.to_list() if df.columns.to_list().count(column_name) > 1]
    return duplicates

def safe_dataframes_to_excel(dataframes: list,
                             sheet_names: list,
                             folder_to_save=os.path.join(r'/Users/ivanov.ev/Work/Dashboard', 'tmp'),
                             file_name='untitled'):
    today_date = date.today().strftime("%d%m%Y")

    try:

        with pd.ExcelWriter(f'{folder_to_save}/{file_name}_{today_date}.xlsx') as writer:

            for df, sheet_name in zip(dataframes, sheet_names):
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    except OSError:

        os.mkdir(folder_to_save)

        with pd.ExcelWriter(f'{folder_to_save}/{file_name}_{today_date}.xlsx') as writer:

            for df, sheet_name in zip(dataframes, sheet_names):
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    finally:

        print(f'File "{file_name}" has been saved to "{folder_to_save}"')


def programme_filling(df: pd.DataFrame):
    df['input_file_name'] = df['inputfile'].apply(lambda x: x[0:x.find('.')])
    df['programme'] = np.where(df['programme'].isnull(), df['input_file_name'], df['programme'])
    df.drop('input_file_name', axis=1, inplace=True)
    return df


def numerated_list(func):
    def wrapper(arg):
        folder_list = func(arg)
        print()
        print(f'Files in "{arg}" displayed below')
        print('--------------')
        for ind, file in enumerate(folder_list):
            print(ind + 1, '. ', file, sep='')
        print('--------------')
        print()

        return folder_list

    return wrapper


@numerated_list
def list_files_in_folder(folder_path_to_list):
    tmp, correct_list = [], []
    garbage_parts = ['.DS', '~']
    scr = 0

    tmp = [file for file in os.listdir(folder_path_to_list) if
           not os.path.isdir(os.path.join(folder_path_to_list, file))]

    for file in tmp:
        scr = 0
        for part in garbage_parts:
            if part in file:
                scr += 1
        if scr == 0:
            correct_list.append(file)

    return correct_list


def select_table_to_filelist(folder_path_to_list, sheet_name=None):
    try:
        file_list = list_files_in_folder(folder_path_to_list)

    except FileNotFoundError:
        print(Fore.RED + 'WARNING: There is no file in specified directory' + Style.RESET_ALL)
        sys.exit()

    # Input file number from displayed list and load Excel file
    file_number = int(input('Which file do you want to download (input a number above): '))
    df = pd.read_excel(os.path.join(folder_path_to_list, file_list[file_number - 1]), sheet_name=sheet_name)

    return df


def groupby_key_field(df: pd.DataFrame, key: list, column_name='value', aggr_func='sum'):
    # Incorrect function

    df = df.set_index(key).groupby(by=key).sum()
    df = df.reset_index()

    return df


def unstack_columns(df: pd.DataFrame, index: list, unstack_column_name: str, value_column_name='value'):
    df = df.groupby(index).agg({value_column_name: 'sum'}).unstack(level=unstack_column_name,
                                                                   fill_value=0).reset_index()
    df.columns = [i[0] if i[0] != value_column_name else i[1] for i in df.columns.to_list()]
    return df


def rename_dict(a_list: list, dictionary: dict, minscore: int):
    # TODO
    # if column has not been found or score equals then store name to mapping
    score = 0
    zeros = 0
    tmp_dict = {}
    dict_for_rename = {}

    # cols_default = [col for col in column_name.unique().tolist() if str(col) != 'nan']
    cols_default = [col for col in set(a_list) if str(col) != 'nan']
    cols_lower = [col.lower() for col in cols_default]
    for col_1, col_2 in zip(cols_default, cols_lower):
        for key, val in dictionary.items():
            for part in val:
                # if col_2.__contains__(part):
                if part in col_1:
                    score += 1
                if part in col_2:
                    score += 1
            tmp_dict[key] = score
            score = 0

        for value in tmp_dict.values():
            if value != 0:
                zeros += 1

        if zeros == 0 or max(tmp_dict.values()) < minscore:
            max_score_name = 'not found'
        else:
            max_score_name = max(tmp_dict, key=tmp_dict.get)

        dict_for_rename[col_1] = max_score_name
        zeros = 0
        tmp_dict = {}

    return dict_for_rename

if __name__ == '__main__':

    import settings

    folder_path = settings.fem_extract
    check_files_list(folder_path)