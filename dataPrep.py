import os
import sys
import pandas as pd
import numpy as np
import math
import main
from warnings import filterwarnings
import func


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

programmes_dict = {
    'ЦЭк': ['цифров', 'эконом', 'цэк'],
    'Pro-Р': ['pro', 'развитие', 'pro-р'],
    'КГ': ['когнит', 'геол', 'кг'],
    'АБ1': ['долгоср','разв','аб', 'др', '1'],
    'АБ2': ['форм', 'бизнес', 'кейс', 'фбк', 'аб', '2'],
    'АБ3': ['проект', 'ввод', 'нов', 'мощн', 'пвнм', 'аб', '3'],
    'АБ4': ['реал', 'цикл', 'аб', '4', 'добыч'],
    'АБ5': ['аб', '5', 'удтм', 'добыч', 'тек'],
    'ТОРО': ['ремонт', 'обслуж', 'торо'],
    'ОСИД': ['осид', 'ириос'],
    'ИПА': ['ипа'],
    'ИМА': ['има'],
    'Экосистема': ['экос', 'система'],
    'СГ': ['цифр', 'сбыт', 'газ', 'сг'],
    'ЦЭ': ['цифр', 'энерг', 'цэ'],
    'ГБ': ['цифр', 'газ', 'бизнес', 'гб'],
    'УПД': ['управл', 'дан', 'упд'],
    'ДТР': ['дирек', 'техн', 'разв', 'тех', 'лаб', 'дтр'],
    'УВП': ['управ', 'взаим', 'подряд', 'увп'],
    'ЦИО': ['цио']
}

subtypecf_dict = {
    'capex': ['capex', 'кап', 'влож'],
    'opex': ['opex'],
    'opex_capital': ['opex', 'кап'],
    'service': ['серв', 'opex'],
    'tax': ['налог', 'ннп']
}

typecf_dict = {
    'umv': ['косв', 'umv'],
    'dmv': ['труд', 'триэ', 'dmv'],
    'npv': ['прям', 'npv'],
    'costs': ['затр']
}

def apply_map(column_name: pd.Series, dictionary: dict):

    new_col = column_name.map(dictionary)
    mapped_column = pd.Series(np.where(new_col.isnull(), column_name, new_col))
    mapped_column.set_axis(new_col.index, inplace=True)

    return mapped_column

def code_preparing(df: pd.DataFrame):
    # TODO try to handle nan values
    # df.code
    # Format U200005258, BI.17.001749_00

    # Find incorrect code length
    df['code_length_test'] = df['code'].astype(str).map(len)
    df.loc[df['code_length_test'] >= 5, 'code'] = df.code
    df.loc[df['code_length_test'] < 5, 'code'] = np.nan


    # One project name - one project code
    incorrect_codes = []

    project_names = df.project.unique().tolist()
    find_incorrect_codes = dict()
    for name in project_names:
        find_incorrect_codes[name] = None

    for project_name in project_names:
        code_values = df.loc[df.project == project_name, 'code'].unique().tolist()
        find_incorrect_codes[project_name] = code_values

    for project_name in find_incorrect_codes.keys():
        if len(find_incorrect_codes[project_name]) == 1:
            incorrect_codes.append(find_incorrect_codes[project_name])

    df.drop('code_length_test', axis=1, inplace=True)
    return df

def programme_preparing(df: pd.DataFrame):

    df['input_file_name'] = df['inputfile'].apply(lambda x: x[0:x.find('.')])
    df['programme'] = np.where(df['programme'].isnull(), df['input_file_name'], df['programme'])
    df.drop('input_file_name', axis=1, inplace=True)
    return df


if __name__ == '__main__':

    filterwarnings('ignore', category=UserWarning, module='openpyxl')

    df = fem.select_table_to_filelist(
        folder_path_to_list=os.path.join(main.base_location, f'fem/loading/{main.version}/preprocessing'),
        sheet_name=main.sheet_name
    )


    # Processing for programme column
    df = programme_preparing(df)
    df.programme = apply_map(df.programme, rename_dict(df.programme, programmes_dict))

    # Processing for typecf column
    df.typecf = apply_map(df.typecf, rename_dict(df.typecf, typecf_dict))
    df['tmp'] = np.where(df.typecf == 'costs', df.subtypecf, df.typecf)
    df.tmp = apply_map(df.tmp, rename_dict(df.tmp, subtypecf_dict))
    df.typecf = np.where(df.typecf == 'costs', df.tmp, df.typecf)
    df = df.drop(labels='tmp', axis='columns')

    # Find problems
    problems = df[df.applymap(lambda x: str(x) == 'nan' or str(x) == 'not found').any(axis=1)]

    # safe preprocessing results
    folder_to_save = os.path.join(main.base_location, f'fem/processing/{main.version}')
    func.safe_dataframes_to_excel(dataframes=[df, problems],
                                  sheet_names=['Основной лист', 'problems'],
                                  folder_to_save=folder_to_save,
                                  file_name='processing')
