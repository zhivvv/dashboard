import func
import os
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style, Back
import time

# From settings file
version = '6+6'
base_location = r'/Users/ivanov.ev/Work/Dashboard/'
sheet_name = 'Основной лист'

files_location = 'fem/loading/' + version
location = os.path.join(base_location, files_location)

# Data preprocessing

if __name__ == '__main__':

    df = None
    errors = {}
    performed_df = None
    fem_folder = os.path.join(base_location, files_location)

    filelist = func.list_files_in_folder(fem_folder)

    func_list = [
        func.drop_columns_with_old_part, func.transform_fem_to_format, func.melt_year_column,
        func.drop_zeros_and_nan_values, func.apply_unit_to_value, func.add_extracting_time_info,
        func.tmp
                 ]

    print('--------------')
    print('Preprocessing has started')

    for filename in filelist:

        print('--------------')
        print(filename)
        print('--------------')
        print(f'Extracting has just been started for {filename}')

        try:

            df = func.extract_fem_from_excel_file(os.path.join(fem_folder, filename), sheet_name=sheet_name)

            if df is None:
                print()
                continue

            print(Fore.GREEN + 'Extracted successfully' + Style.RESET_ALL, end='')
            print()
            print('Preprocessing...')
            time.sleep(0.01)

        except Exception as e:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL, end='')
            print()
            continue

        for func in tqdm(func_list):
            try:
                tmp = func(df)
                time.sleep(0.01)
                if tmp is not None:
                    df = tmp
                else:
                    print(Fore.GREEN + 'df became None on ' + func + Style.RESET_ALL)
                    df = None
                    break

            except Exception as e:

                print(Fore.RED + 'ETL failed')
                print(func)
                print(e)
                print(Style.RESET_ALL)
                df = None
                break

        if df is None:
            continue

        df = func.add_edit_time_info(df, fem_folder=fem_folder, filename=filename)
        time.sleep(0.01)
        df['inputfile'] = filename
        time.sleep(0.01)
        df['version'] = version
        time.sleep(0.01)

        if performed_df is None:
            performed_df = df
        else:
            performed_df = pd.concat([performed_df, df], axis=0)

        print(Fore.GREEN + f'Preprocessing "{filename}" successfully complete' + Style.RESET_ALL)
        print()

    performed_df.reset_index(inplace=True, drop=True)
    performed_df.reset_index(inplace=True, drop=False)

    # Find problems
    problems = None
    # problems = df[df.applymap(lambda x: str(x) == 'nan').any(axis=1)]
    problems = performed_df[performed_df.applymap(lambda x: str(x) == 'nan').any(axis=1)]
    time.sleep(0.01)

    # Save file after preproccesing
    print('--------------')
    print('File saving')
    print('--------------')
    folder_to_save = os.path.join(base_location, f'fem/loading/{version}/preprocessing')
    func.safe_dataframes_to_excel(dataframes=[performed_df, problems],
                                 sheet_names=['Основной лист', 'problems'],
                                 folder_to_save=folder_to_save,
                                 file_name='preprocessing')

    # Check information in columns - call check_column_info
    # print(pd.DataFrame.from_dict(errors))
    print(Fore.GREEN + 'Preprocessing successfully ended' + Style.RESET_ALL)
