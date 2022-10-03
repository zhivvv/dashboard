import os.path
import time
from os import path
import func
import settings
from settings import base_location, version, sheet_name
import pandas as pd
import traceback as tb
import numpy as np
from func import rename_dict
import datetime
from colorama import Fore, Style, Back

def decorator_entire_process(main_process):

    @func.timer
    def wrapper():
        print('--------------')
        print('Process started')
        print('--------------')
        result = main_process()
        print('Process ended')
        return result

    return wrapper


def decorator_file_preparing(extraction_transform_process):
    def wrapper(file_path):
        print(os.path.basename(file_path), ' ... ', end=' ')
        start = datetime.datetime.now()
        result = extraction_transform_process(file_path)
        end = datetime.datetime.now()
        print(Fore.GREEN, 'ok', Style.RESET_ALL, ' (', end - start, ')', sep='')
        return result

    return wrapper


@decorator_entire_process
def extraction_process():
    errors = dict()
    result_df = None

    for file in func.check_files_list(settings.fem_extract):
        try:
            fem = fem_preparing(os.path.join(settings.fem_extract, file))
        except Exception as e:
            print(Fore.RED, 'not ok', Style.RESET_ALL)
            errors[file] = ''.join(tb.format_exception(None, e, e.__traceback__))
            continue

        result_df = pd.concat([result_df, fem], axis=0)

    if len(errors) > 0:
        print('-------------')
        for file, err in errors.items():
            print(file)
            print(err)


@decorator_file_preparing
def fem_preparing(file_path):
    fem = pd.ExcelFile(file_path).parse(sheet_name=settings.sheet_name)
    return FemTransform(fem).transform()


class FemTransform:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def skip_top_rows_in_dataframe(self):

        columns_to_find = [2022, 2023, 2024]

        for ind, row in self._df.iterrows():
            if set(columns_to_find) - set(row) == set() or set(columns_to_find) - set(row.index) == set():

                if ind == 0:
                    return self
                else:
                    self._df.columns = self._df.iloc[ind, :].tolist()
                    self._df = self._df.iloc[ind + 1:, :]

                    return self
        raise

    def correct_column_names_for_dataframe(self):

        def find_year_columns(df: pd.DataFrame):

            YEAR_START, YEAR_END = 2000, 2100

            year_columns = dict()
            year_range = range(YEAR_START, YEAR_END)
            for column_name in df.columns:
                try:
                    value = int(column_name)
                    if value in year_range:
                        year_columns[column_name] = value

                except:
                    continue

            return year_columns

        def drop_columns_with_bad_part(dictionary: dict):

            BAD_PARTS = ['old', '__']

            result_dictionary = dictionary.copy()

            for column_name in dictionary:
                for part in BAD_PARTS:
                    if part in column_name:
                        result_dictionary.pop(column_name)

            return result_dictionary

        def find_categorical_columns(df: pd.DataFrame):

            categorical_columns = dict()

            column_fragments = {
                'programme': ['прог', 'Прог', 'ИСУП', 'исуп'],
                'code': ['код', 'Код', 'ИСУП', 'исуп'],
                'project': ['назв', 'проект', 'Назв', 'ИСУП', 'исуп'],
                'subtypecf': ['подтип', 'выбрать', 'Подтип', 'cf'],
                'typecf': ['выбрать', 'Тип', 'cf', 'CF'],
                'dzo': ['до', 'ДО', 'ДО'],
                'unit': ['изм', 'Ед', 'ед. изм.']
            }

            cat_data = [col for col in df.columns if isinstance(col, str)]
            cols_dict = rename_dict(cat_data, column_fragments, minscore=3)
            cols_dict = drop_columns_with_bad_part(cols_dict)
            tmp = [i for i in cols_dict if cols_dict[i] != 'not found']
            for i in tmp:
                categorical_columns[i] = cols_dict[i]

            return categorical_columns

        def check_columns_in_dataframe(_list: list):

            correct_set = {'programme', 'project', 'code', 'typecf', 'subtypecf', 'dzo', 'unit'}

            if set(correct_set) - set(_list) == set() and len(_list) == len(correct_set):
                pass
            else:
                raise

        try:
            columns_for_rename = find_categorical_columns(self._df)
            check_columns_in_dataframe(list(columns_for_rename.values()))
        except:
            raise

        columns_for_rename.update(find_year_columns(self._df))
        self._df = self._df[list(columns_for_rename)].rename(columns=columns_for_rename)

        return self

    def drop_incorrect_values(self):

        def float_check(value):
            try:
                value = float(value)
            except:
                value = np.nan
            return value

        def apply_float_check(df: pd.DataFrame, column_name):
            df[column_name] = df[column_name].apply(lambda x: float_check(x))
            return df

        self._df = (self._df
                    .dropna(how='all')
                    .loc[:, ~(self._df == 0).all()]
                    .pipe(apply_float_check, 'value')
                    .dropna(subset=['value', 'project'])
                    .loc[~(self._df['value'] == 0)]
                    )

        return self

    def melt_year_column(self):

        # Before melting columns function requires to get rid of duplicates in header
        def check_duplicate_column_name(df: pd.DataFrame):
            duplicates = [col_name for col_name in df.columns.to_list() \
                          if df.columns.to_list().count(col_name) > 1]
            if len(duplicates):
                return True

        if check_duplicate_column_name(self._df):
            raise

        # Find column where values are placed

        id_vars = ['programme', 'code', 'project', 'typecf', 'subtypecf', 'dzo', 'unit']

        self._df = pd.melt(self._df,
                           id_vars=id_vars,
                           var_name='year',
                           value_name='value'
                           )

        self._df['year'] = self._df['year'].astype('int')

        return self

    def trim_all_columns(self):

        cols = []
        df_dtypes = self._df.dtypes.to_dict()

        for column_name in df_dtypes.keys():
            if df_dtypes[column_name] == 'int' or df_dtypes[column_name] == 'float':
                continue
            cols.append(column_name)

        self._df[cols] = self._df[cols].apply(lambda x: x.str.strip())
        return self

    def apply_unit_to_value(self):
        # TODO try to rewrite function with TRY EXCEPT

        df = self._df

        df.value = df.value.apply(lambda x: x if isinstance(x, float) + isinstance(x, int) == 1 else np.nan)
        df.value = df.value.apply(lambda x: float(x))
        values = df.unit.value_counts(dropna=False)

        # if np.nan in values.keys():
        #     print(Fore.RED + 'Where are nan values in unit column' + Style.RESET_ALL)

        main_unit = values.idxmax()
        df.unit.fillna(main_unit)

        if df['unit'].str.contains('тыс').any():
            df['value'] = df['value'] / 1000

        df.drop('unit', axis=1, inplace=True)

        self._df = df

        return self

    def transform(self):

        (self
         .skip_top_rows_in_dataframe()
         .correct_column_names_for_dataframe()
         .melt_year_column()
         .drop_incorrect_values()
         .apply_unit_to_value()
         )

        return self._df


if __name__ == '__main__':
    extraction_process()

