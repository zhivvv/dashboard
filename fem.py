# import xlrd, xlwings
import os.path  # path.splitext
from warnings import filterwarnings
import pandas as pd  # modules: read_excel

import main

filterwarnings('ignore', category=UserWarning, module='openpyxl')


def extract_fem_from_excel_file(file_location, sheet_name, row_to_skip=0):
    list_of_possible_extensions_for_pandas = ['.xlsx', '.xls', '.xlsm', '.xlsb']
    file_extension = os.path.splitext(file_location)[1].lower()

    if file_extension in list_of_possible_extensions_for_pandas:
        df = pd.read_excel(file_location,
                           sheet_name=sheet_name,
                           skiprows=row_to_skip
                           )

        # Column name to string
        df.columns = df.columns.astype(str)
        # Drop "Unnamed" columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
        # Drop all columns where value is nan
        df = df.dropna(axis='columns', how='all')
        # Trim column names
        df = df.rename(columns=lambda x: x.strip())
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    else:
        # add file_name
        df = 'can\'t be read'

    return df


def melt_year_column(fem_df: pd.DataFrame):
    id_vars = ['Программа (ИСУП)',
               'Код проекта (ИСУП)',
               'Название проекта (ИСУП)',
               'Тип CF (выбрать из списка)',
               'Подтип CF (выбрать из списка)',
               'ДО',
               'Ед. изм.'
               ]

    fem_df = pd.melt(fem_df,
                     id_vars=id_vars,
                     var_name='Год',
                     value_name='Значение'
                     )

    # Drop garbage in year column
    fem_df['year_check'] = fem_df['Год'].apply(lambda x: 'True' if float_check(x) else 'False')
    fem_df = fem_df[fem_df['year_check'] == 'True']
    fem_df.drop('year_check', axis=1, inplace=True)

    # Drop garbage in value column
    fem_df['value_check'] = fem_df['Год'].apply(lambda x: 'True' if float_check(x) else 'False')
    fem_df = fem_df[fem_df['value_check'] == 'True']
    fem_df.drop('value_check', axis=1, inplace=True)

    # Make value column as float type
    fem_df['Значение'] = fem_df['Значение'].astype(float)

    # Drop NaN values and zeros
    fem_df.dropna(subset=['Значение'], inplace=True)
    fem_df = fem_df[fem_df['Значение'] != 0]

    return fem_df


def float_check(value):
    try:
        return type(float(value)) == float
    except ValueError:
        return False


def apply_unit_to_value(df: pd.DataFrame):
    if df['Ед. изм.'].str.contains('тыс').any():
        df['Значение'] = df['Значение'] / 1000

    df.drop('Ед. изм.', axis=1, inplace=True)

    return df


def calculations(df: pd.DataFrame):
    df['Затраты'] = df['CAPEX'] + df['OPEX']
    a_index = df['OCF'].cumsum().argmin()
    return sum(df['OPEX'].iloc[0:a_index + 1])


def save_file(df: pd.DataFrame, file_name=None, file_type='tmp'):
    file_loc = os.path.join(os.path.expanduser('~'), main.files_location, file_type, f'{file_name}.xlsx')

    try:
        df.to_excel(file_loc, index=False)
    except FileNotFoundError:
        path = os.path.join(os.path.expanduser('~'), main.files_location, file_type)
        os.mkdir(path)
        df.to_excel(file_loc, index=False)


def unstack_column(df: pd.DataFrame, column_name):
    index = ['Программа (ИСУП)', 'Код проекта (ИСУП)',
             'Название проекта (ИСУП)', 'Тип CF (выбрать из списка)',
             'ДО', 'Год'] + [column_name]
    df = df.groupby(index).sum()
    df = df.reset_index().set_index(index)
    df = df.unstack(column_name).reset_index()
    df.fillna(0, inplace=True)
    return df


def flatten_columns(df):
    new_cols = []
    for a_col in df.columns:
        new_cols.append(a_col[0] if a_col[1] == '' else a_col[1])
    df.columns = new_cols
    return df


def apply_mapping_to_column(column_name):
    # Сделать проверку по методу из почты (Родион)
    pass


def find_column_name_row(df: pd.DataFrame):
    # To skip top rows in file
    pass


def pretty_print(df):
    with pd.option_context('display.max_columns', 0, 'display.max_rows', 0, 'display.width', 10000):
        print(df)


def select_effect(df, effect_type):
    return df[df['Тип CF (выбрать из списка)'] == effect_type]

required_cols = {
        "Сокращение расходов на оплату труда ": "ТРЗ",
        "Сокращение CAPEX": "Сокращение CAPEX",
        "Сокращение OPEX": "Сокращение OPEX",
        "Изменение денежного потока от увеличения добычи/реализации УВ": "ДП от УВ",
        "Ранняя добыча / ранняя нефть": "Ранняя нефть",
        "Повышение доходов от оказания услуг либо продажи продукции (за исключением нефти, газа и нефтепродуктов)": "ДП от других продаж",
        "Митигация рисков": "Митигация рисков",
        "Прочее": "Прочее",
        "Капитальные затраты (CAPEX):": "CAPEX",
        "Операционные затраты (OPEX):капитализируемые": "OPEX кап",
        "Операционные затраты (OPEX):": "OPEX некап",
        "ННП": "ННП пр",
        "ННП (для расчета по косв. Эффектам и ТРИЭ)": "ННП кос",
        "Сервис": "Сервис"
    }

def add_columns(df):


    for a_col in required_cols:
        if a_col not in df.columns:
            df[a_col] = 0.
    new_cols = [required_cols[a] if a in required_cols else a for a in df.columns]
    df.columns = new_cols
    return df


def fem(df):

    direct_effect_filter = (df['Тип CF (выбрать из списка)'] == 'Прямой эффект') * 1.
    costs_filter = (df['Тип CF (выбрать из списка)'] == 'Затраты') * 1.

    df['CF'] = 0
    for a_col in required_cols.values():
        df['CF'] += df[a_col]

    df['+CF'] = df["CF"] * direct_effect_filter
    df['-CF'] = -df['CF']
    df['-CF'] += df['ННП кос']
    df['-CF'] *= costs_filter


    df['OCF'] = 0
    for a_col in ['Дополнительный доход', 'Налог', 'Оптимизация затрат', 'Прочее',
       'Трудозатраты']:
        df['OCF'] += df[a_col]
    for a_col in ['CAPEX', 'OPEX']:
        df['OCF'] -= df[a_col]

    if 'Сокращение CAPEX' in df.columns:
        df['OCF_new'] =- direct_effect_filter * df['Сокращение CAPEX']
    return df