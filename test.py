# data = {'version': ['6+6'], 'base_location': ['/Users/ivanov.ev/Work/Dashboard/']}
#
# df = pd.DataFrame(data)
# path = '/Users/ivanov.ev/Work/Dashboard/config/config.json'
# # df.to_json(path_or_buf=path)
# df = pd.read_json(path)
#
# version = df['version'].dropna().tolist()
# base_location = df['base_location'].dropna().tolist()
# sheet_name = df['sheet_name'].tolist()
#
# print(version, base_location, sheet_name, sep='\n')

import pandas as pd
import main
import os
import fem

# path_to_folder = os.path.join(main.base_location, 'fem', 'processing', main.version)

# df = fem.select_table_to_filelist(folder_path_to_list=path_to_folder,
#                                   sheet_name=main.sheet_name)

sheet_info_name = 'load'
file_name = 'ЦЭк.xlsx'
path_to_folder = os.path.join(main.base_location, 'fem', 'loading', main.version)

header = ['key']
years = [i for i in range(2015, 2051)]
header += years

info = pd.read_excel(io=os.path.join(path_to_folder, file_name),
                   sheet_name=sheet_info_name
                   )

for project_name ,sheet_name in zip(info.project, info.sheet):

    df = fem.extract_fem_from_excel_file(file_path=os.path.join(path_to_folder, file_name),
                                         sheet_name=sheet_name)
    new_header = list(set(df.columns) & set(header))

    df = df.loc[~df['key'].isnull(), new_header]
# def find_year_of_min_effect(df: pd.DataFrame, granula: str):

    # Step 1 - Remain only effect rows
    # df = df.loc[(df['typecf'] == 'umv') | (df['typecf'] == 'npv') | (df['typecf'] == 'dmv'), [granula, 'year']]

    # Step 2 - Aggregation according to choice
    # min_year_with_effect = df.groupby(by=[granula]).agg({'year': 'min'}).rename(columns={'year': 'min_year'})

    # # Step 3 - Find year of start amortization
    # df = df.join(min_year_with_effect, on=granula, how='left')

    # return min_year_with_effect

# index = ['programme', 'code', 'project', 'typecf', 'year', 'dzo', 'subtypecf']
# unstack_column = 'subtypecf'
# value_column_name = 'value'

# df = fem.unstack_columns(df, index, unstack_column, value_column_name)

# fem.safe_dataframes_to_excel([tmp], ['tmp'])

# Amortization calculations
# granula = 'project'
# min_year = find_year_of_min_effect(df, granula=granula)
# df = df.join(min_year, on=granula, how='left')

# Step 5 - Create new column "Ввод новых ОФ"
# df['ВводновыхОФ'] = df

# df['vvod_novykh_of'] = df.loc[
#     (df['subtypecf'] == 'capex') | (df['subtypecf'] == 'opex_capital'),
#     ['value']
#     ]

# tmp_df = df.loc[:,['code', 'project', 'subtypecf', 'year', 'vvod_novykh_of']]


