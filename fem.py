# import xlrd, xlwings
from colorama import Fore, Style, Back
import os.path
import math
import pandas as pd
import numpy as np
import main
from datetime import date
from warnings import filterwarnings
import datetime
import builtins
import traceback
import sys



filterwarnings('ignore', category=UserWarning, module='openpyxl')

def tmp(df: pd.DataFrame):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def apply_unit_to_value(df: pd.DataFrame):

    # TODO try to rewrite function with TRY EXCEPT

    df.value = df.value.apply(lambda x: x if isinstance(x, float) + isinstance(x, int) == 1 else np.nan)
    df.value = df.value.apply(lambda x: float(x))
    values = df.unit.value_counts(dropna=False)

    if np.nan in values.keys():
        print(Fore.RED + 'Where are nan values in unit column' + Style.RESET_ALL)

    main_unit = values.idxmax()
    df.unit.fillna(main_unit)

    if df['unit'].str.contains('тыс').any():
        df['value'] = df['value'] / 1000

    df.drop('unit', axis=1, inplace=True)

    return df

def skip_garbage_top_rows(df: pd.DataFrame):
    # To skip top rows in file

    if not isinstance(df, pd.DataFrame):
        print(Fore.RED + 'Data is not valid. Cannot find rows to skip' + Style.RESET_ALL)
        return

    column_fragments = [2022, 2023, 2024]
    test_list = []

    for row in df.iterrows():
        if row[0] == 0:
            for column_name in column_fragments:
                if column_name in row[1].index.to_list():
                    test_list.append(column_name)
            if test_list == column_fragments:
                row_to_skip = 0
                return row_to_skip
            else:
                test_list = []
        for column_name in column_fragments:
            if column_name in row[1].to_list():
                test_list.append(column_name)
        if test_list == column_fragments:
            row_to_skip = row[0] + 1
            return row_to_skip
        else:
            test_list = []

    return -1

def extract_fem_from_excel_file(file_path, sheet_name=0):
    list_of_possible_extensions_for_pandas = ['.xlsx', '.xls', '.xlsm', '.xlsb']
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in list_of_possible_extensions_for_pandas:
        print(Fore.RED + f'Error in file {file_name}: invalid file extension' + Style.RESET_ALL)
        return

    try:
        sheet_names = pd.ExcelFile(file_path).sheet_names
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        return

    if sheet_name in sheet_names:

        df = pd.read_excel(file_path, sheet_name=sheet_name)
        rows_to_skip = skip_garbage_top_rows(df)
        if rows_to_skip > 0:
            rows_to_skip -= 1
            df.columns = df.iloc[rows_to_skip]
            df = df[rows_to_skip + 1:]
        elif rows_to_skip == 0:
            pass
        else:
            print(Fore.RED + 'Header did not found' + Style.RESET_ALL)
            return

    else:
        print(Fore.RED + 'Sheet {sheet_name} in {file_name} did not found' + Style.RESET_ALL)
        return

    # Successful
    return df

def drop_columns_with_old_part(df: pd.DataFrame):

    cols = df.columns
    old_contain = cols.str.contains('old').to_list()
    new_cols = [col if not math.isnan(col) else False for col in old_contain]
    new_cols = [False if col else True for col in new_cols]

    correct_cols = cols[new_cols]

    df = df[correct_cols]
    return df

def drop_zeros_and_nan_values(df: pd.DataFrame):
    # TODO Replace 0x17 to function that checks values
    df = df[(df['value'] != 0) & (df['value'] != '0x17') & (df['value'] != '0xf')]
    df = df.dropna(subset='value')

    return df

def check_int_values(value):
    try:
        if int(value) > 2000:
            return int(value)
        else:
            return value
    except:
        return value

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

def int_value_or_not(value):
    try:
        value = int(value)
        return value
    except:
        return value

def transform_fem_to_format(df: pd.DataFrame):

    if type(df) != pd.DataFrame:
        print(Fore.RED + 'DataFrame is not valid' + Style.RESET_ALL)
        return

    # Check values
    correct_column_list = []
    for column_name in df.columns:
        correct_column_list.append(check_int_values(column_name))
    df.columns = correct_column_list

    # Column name to string
    df.columns = df.columns.astype(str)
    # Drop "Unnamed" columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
    # Drop all columns where value is nan
    df = df.dropna(axis=1, how='all')
    # Trim column names
    df = df.rename(columns=lambda x: x.strip().lower())
    # Trim column names
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    column_fragments = {
        'прог': 'programme',
        'код': 'code',
        'название п': 'project',
        'подтип': 'subtypecf',
        'тип': 'typecf',
        'до': 'dzo',
        'изм.': 'unit'
    }

    list_to_iterate = list(column_fragments.keys()).copy()

    length_of_dict = len(column_fragments)
    dict_to_rename = {}

    for fragment in list_to_iterate:
        for column_name in df.columns:
            if fragment in column_name and 'old' not in column_name:
                dict_to_rename[column_name] = column_fragments[fragment]
                column_fragments.pop(fragment)
                break

    if len(column_fragments) != 0 and len(dict_to_rename) != length_of_dict:
        print(Fore.RED + 'Column rename error' + Style.RESET_ALL)
        return None
    df.rename(columns=dict_to_rename, inplace=True)

    # Switch type to years to int
    correct_column_list = []
    for column_name in df.columns:
        correct_column_list.append(check_int_values(column_name))
    df.columns = correct_column_list

    columns_format_fem = []
    for column_name in df.columns:
        if column_name in dict_to_rename.values() or isinstance(column_name, int):
            columns_format_fem.append(column_name)

    df = df[columns_format_fem]
    df = df.loc[:, ~(df == 0).all()]

    df = df[(~df.code.isnull()) | (~df.programme.isnull()) | (~df.project.isnull())]

    return df

def trim_all_columns(df: pd.DataFrame):
    cols = []
    df_dtypes = df.dtypes.to_dict()
    for column_name in df_dtypes.keys():
        if df_dtypes[column_name] == 'int' or df_dtypes[column_name] == 'float':
            continue
        cols.append(column_name)

    df[cols] = df[cols].apply(lambda x: x.str.strip())
    return df

def check_duplicate_column_name(df: pd.DataFrame):
    duplicates = [column_name for column_name in df.columns.to_list() if df.columns.to_list().count(column_name) > 1]
    return duplicates

def melt_year_column(df: pd.DataFrame):

    if type(df) != pd.DataFrame:
        # print('--Error in "melt_year_column". Input is not a DataFrame')
        return None

    # Before melting columns function requires to get rid of duplicates in header

    check = check_duplicate_column_name(df)

    if len(check) == 0:

        # Find column where values are placed

        id_vars = ['programme',
                   'code',
                   'project',
                   'typecf',
                   'subtypecf',
                   'dzo',
                   'unit'
                   ]

        df = pd.melt(df,
                     id_vars=id_vars,
                     var_name='year',
                     value_name='value'
                     )

        df['year'] = df['year'].astype('int')

        return df

    else:
        # print(f'--Header has duplicates - {check}. Try to rename columns in input file')
        return None

def float_check(value):
    try:
        return type(float(value)) == float
    except ValueError:
        return False

def safe_dataframes_to_excel(dataframes:list,
                             sheet_names:list,
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

    garbage = ['.DS_Store']
    correct_list = [file for file in os.listdir(folder_path_to_list) if file not in garbage and
                    not os.path.isdir(os.path.join(folder_path_to_list, file))]

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

def groupby_key_field (df: pd.DataFrame, key: list, column_name='value', aggr_func='sum'):

    df = df.set_index(key)
    df = df.groupby(by=key).agg({column_name: aggr_func})
    df = df.reset_index()

    return df

def unstack_columns(df: pd.DataFrame, index: list, unstack_column_name: str, value_column_name='value'):
    df = df.groupby(index).agg({value_column_name: 'sum'}).unstack(level=unstack_column_name, fill_value=0).reset_index()
    df.columns = [i[0] if i[0] != value_column_name else i[1] for i in df.columns.to_list()]
    return df