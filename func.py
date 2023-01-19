from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzz_process
from colorama import Fore, Style
import os.path
import pandas as pd
from datetime import date
from warnings import filterwarnings
import datetime
import time
import settings
import pyinputplus as pyip

filterwarnings('ignore', category=UserWarning, module='openpyxl')


class File:

    def __init__(self, file_path):
        self.path = file_path

    def get_file_size(self):
        bytes_in_megabyte = 1024 * 1024
        size = os.path.getsize(self.path) / bytes_in_megabyte
        return size

    def get_create_date(self):
        # s1 = path.getctime(file_path)
        s1 = os.stat(self.path).st_birthtime
        s2 = datetime.datetime.strptime(time.ctime(s1), '%c').date()
        s3 = s2.strftime('%d/%m/%Y')
        return s3

    def get_mod_date(self):
        s1 = os.path.getmtime(self.path)
        s2 = datetime.datetime.strptime(time.ctime(s1), '%c').date()
        s3 = s2.strftime('%d/%m/%Y')
        return s3

    def add_extracting_time_info(self, df: pd.DataFrame):
        extract_timestamp = datetime.datetime.now()

        df['extracting_date'] = extract_timestamp.strftime('%d.%m.%Y')
        df['extracting_time'] = extract_timestamp.strftime('%H:%M')

        return df

    def add_edit_time_info(self, df: pd.DataFrame, fem_folder, filename):
        edit_timestamp = os.path.getmtime(os.path.join(fem_folder, filename))
        datestamp = datetime.datetime.fromtimestamp(edit_timestamp)

        df['edit_date'] = datestamp.strftime('%d.%m.%Y')
        df['edit_time'] = datestamp.strftime('%H:%M')

        return df


class Folder:

    @staticmethod
    def __isdir_check(x):
        check = os.path.isdir(x)
        if not check:
            raise IsADirectoryError
        else:
            return x

    def __init__(self, folder_path: str):
        self.path = Folder.__isdir_check(folder_path)
        self.name = os.path.basename(folder_path)

    @property
    def files(self) -> list | str:

        wrong = ['~$']
        file_list = []

        try:
            for file in os.listdir(self.path):
                for bad in wrong:
                    if not os.path.isdir(os.path.join(self.path, file)) and bad not in file:
                        file_list.append(file)

            return file_list

        except FileNotFoundError:
            print(Fore.RED + 'Specified directory has not been found' + Style.RESET_ALL)

    @property
    def excel_files(self):

        excel_extension = '.xls'
        files_list = [file for file in self.files if excel_extension in file]
        return files_list

    def select_file(self, xls=True):
        file_name = pyip.inputMenu(choices=self.excel_files if xls else self.files,
                                   prompt='Files:\n',
                                   numbered=True,
                                   blank=True)

        print('Selected:', Fore.GREEN + file_name + Style.RESET_ALL)
        return file_name

    def file_exists(self, file: str):
        return os.path.exists(os.path.join(self.path, file))


class MatchingProcess:

    def __init__(self, choices: pd.Series | list):
        # default parameters
        self.choices = choices
        self.__score_cutoff_choice = 80
        self.__show_results_in_terminal = False
        self.__drop_not_best = True
        self.__add_column_name = False
        self.__show_matched = False
        self.__percent_result = None

    # getter and setter methods

    @property
    def show_matched(self):
        return self.__score_cutoff_choice

    @show_matched.setter
    def show_matched(self, flag: bool):

        if not isinstance(flag, bool):
            raise ValueError

        self.__show_matched = flag

    @property
    def score_cutoff_choice(self):
        return self.__score_cutoff_choice

    @score_cutoff_choice.setter
    def score_cutoff_choice(self, value: int):

        if value not in range(0, 100):
            raise ValueError

        self.__score_cutoff_choice = value

    @property
    def show_results_in_terminal(self):
        return self.__show_results_in_terminal

    @show_results_in_terminal.setter
    def show_results_in_terminal(self, flag: bool):

        if not isinstance(flag, bool):
            raise ValueError

        self.__show_results_in_terminal = flag

    # Methods

    def single_match(self, query: str, show_max=True, get_score=False) -> dict | tuple | str:
        """
        Description:

        Function returns matching result for one string value.

        :param query: just a word (str) that need to be searched
        :param show_max: return only max result
        :param get_score: matching result (%)
        :return: matching results or one result if show_max is True

        """
        scorers_coef = {fuzz.token_sort_ratio: 0.11,  # 1
                        fuzz.QRatio: 0.11,  # 2
                        fuzz.UQRatio: 0.11,  # 3
                        fuzz.UWRatio: 0.11,  # 4
                        fuzz.WRatio: 0.11,  # 5
                        fuzz.partial_ratio: 0.11,  # 6
                        fuzz.ratio: 0.11,  # 7
                        fuzz.partial_token_set_ratio: 0.11,  # 8
                        fuzz.partial_token_sort_ratio: 0.11  # 9
                        }

        if isinstance(self.choices, pd.Series):
            choices = self.choices.dropna().tolist()
        else:
            choices = self.choices

        results = {x: 0 for x in choices}

        for scorer in scorers_coef:
            match = fuzz_process.extractOne(query=query,
                                            choices=self.choices,
                                            scorer=scorer,
                                            score_cutoff=self.score_cutoff_choice)
            if match is None:
                continue

            results[match[0]] += match[1] * scorers_coef[scorer]

        if show_max:
            res = max(results, key=results.get)
            if get_score:
                return res, max(results.values())
            return res

        return results

    def sequence_match(self, query: list | pd.Series) -> dict:

        result = dict()

        # Get exact structure
        if isinstance(query, pd.Series):
            input_list_process = query.dropna().unique()
        else:
            input_list_process = set([x for x in query if str(x) != 'nan'])

        for name in input_list_process:
            processed_choice = self.single_match(query=name)

            result[name] = processed_choice

        return result


def single_input_file(folder_path):
    list_of_folder_excel_files = check_excel_files_list(folder_path)
    file_number_to_load = pyip.inputNum(min=1, max=len(list_of_folder_excel_files)) - 1
    file_name_to_load = list_of_folder_excel_files[file_number_to_load]

    return file_name_to_load


def check_excel_files_list(folder_path: str) -> list:
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

    return list(set(correct_list))


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


def tmp(df: pd.DataFrame):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def check_duplicate_column_name(df: pd.DataFrame):
    duplicates = [column_name for column_name in df.columns.to_list() if df.columns.to_list().count(column_name) > 1]
    return duplicates


def safe_dataframes_to_excel(dataframes: list,
                             sheet_names: list,
                             folder_to_save=os.path.join(settings.base_location, 'tmp'),
                             file_name='untitled'):
    today_date = date.today().strftime("%d%m%Y")

    def save_process(exist=True):

        path_to_save = f'{folder_to_save}/{file_name}_{today_date}.xlsx'

        if os.path.exists(path_to_save) and exist:
            raise FileExistsError

        with pd.ExcelWriter(path_to_save) as writer:
            for df, sheet_name in zip(dataframes, sheet_names):
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(Fore.GREEN + f'File "{file_name}" has been saved to "{folder_to_save}"' + Style.RESET_ALL)

    try:
        save_process()

    except FileNotFoundError:
        os.mkdir(folder_to_save)
        save_process()
    except FileExistsError:
        print(Fore.YELLOW + f'"{file_name}_{today_date}" exists in "{folder_to_save}"' + Style.RESET_ALL)
        print('Do you want to rename file?')
        choice = pyip.inputYesNo(prompt='(y/n) - ', yesVal='y', noVal='n')
        if choice == 'y':
            file_name = input('file_name: ')
            save_process()
        else:
            save_process(exist=False)


def rename_dict(a_list: list, dictionary: dict, minscore: int):
    # if column has not been found or score equals then store name to mapping
    # todo get rid!
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


def timer(some_process):
    def wrapper(*args, **kwargs):
        time_started = datetime.datetime.now()
        some_process(*args, **kwargs)
        time_finished = datetime.datetime.now()
        process_time = time_finished - time_started  # TODO add time format
        print('(', process_time, ' sec)', sep='')

    return wrapper


def process_decorator(process_function):
    @timer
    def wrapper(*args, **kwargs):
        print('--------------')
        print('Process has just started')
        print('--------------')
        process_function(*args, **kwargs)
        print(Fore.GREEN + 'Finished successfully' + Style.RESET_ALL, end=' ')

    return wrapper

# def read_multiple_excel_files(files_path_list: list, sheet_list: list):
#     # todo move to Folder class
#     dataframe_dictionary = dict()
#
#     for file, sheet_name in zip(files_path_list, sheet_list):
#
#         file_base_name = os.path.basename(file)
#         try:
#             load = pd.ExcelFile(file).parse(sheet_name=sheet_name)
#             dataframe_dictionary[file_base_name] = load
#         except:
#             dataframe_dictionary[file] = None
#             print(f'{file_base_name} has not been loaded')
#             continue
#
#     return dataframe_dictionary


# def save_formulas_to_excel():
#     import openpyxl
#     from openpyxl.cell import Cell
#     from openpyxl import Workbook
#     wb: Workbook = openpyxl.load_workbook(settings.OPENPYXL_EXTRACTION_PATH)
#     ws = wb[settings.openpyxl_sheet_name]
#     cellObj: Cell
#     for i, cellObj in enumerate(ws['C'], 1):
#         if i == 1:
#             continue
#         print(ws['B'][0])
#
#         cellObj.value = "=vlookup(A{0}, A:B, 2, 0)".format(i)
#     wb.save(settings.OPENPYXL_EXTRACTION_PATH)
