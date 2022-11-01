import os
import numpy as np
import pandas as pd
import pyinputplus as pyip
import func
import settings

base_year = 2022
rate = 0.14


def calculation_process():
    # load data
    file_folder = settings.report_folder_results
    file_name = 'full_report_30102022.xlsx'
    df = pd.ExcelFile(os.path.join(file_folder, file_name)).parse()

    # project = 'Openbox'
    granula = 'project'
    column_to_unstack = 'typecf'
    effect = ['npv']

    data = pivot(data=df, column_name=column_to_unstack, granula=granula)

    result = calc_engine(data, granula, effect)

    # data = data[data['project'] == project]
    # data = basic_calculations(data, effect, granula=granula)
    # kpi = kpi_calculations(data, effect, granula=granula)
    # func.safe_dataframes_to_excel([data, kpi], ['data', 'kpi'])
    # print('Process finished')

    return result


def granula_choice():
    list_of_granulas = ['programme', 'project']
    granula = pyip.inputMenu(choices=list_of_granulas, prompt='input granula: ', blank=True)

    return granula


def effect_choice():
    list_of_effect = ['npv', 'umv', 'dmv']
    effect = pyip.inputMenu(choices=list_of_effect, prompt='input effect: ', blank=True)

    return effect


def pivot(data: pd.DataFrame, column_name: str, granula: str):
    column_index = [granula, 'year']

    result = data.pivot_table(values='value',
                              index=column_index,
                              columns='typecf',
                              aggfunc='sum',
                              fill_value=0)

    result.reset_index(inplace=True)
    return result


def kpi_calculations(data: pd.DataFrame, effect: str, granula):

    result = data[[granula, 'dcf', 'pvi']].groupby(granula).sum()
    result['pi'] = result['dcf'] / result['pvi'] + 1

    rename_dict = {'dcf': effect}
    result = result.reset_index().rename(columns=rename_dict)

    return result


def pvi_calculation(data: pd.DataFrame, granula):
    data['aocf'] = data[[granula, 'ocf']].groupby(granula).cumsum()
    data['year_min_aocf'] = data.loc[data['aocf'].idxmin(), 'year']
    data['pvi'] = data['capex'] + data['opex_capital'] + \
                  np.where(data['year'] < data['year_min_aocf'],
                           data['opex'], 0
                           )
    return data


def basic_calculations(data: pd.DataFrame, effect: str, granula):

    data['costs'] = (data['capex'] + data['opex'] + data['opex_capital']
                     + data['tax'] + data['service']
                     )
    data['cf'] = data[effect] - data['costs']
    data['df'] = data['year'].apply(lambda x: pow((1 + rate), (base_year - x - 0.5)))
    data['dcf'] = data['cf'] * data['df']
    data['ocf'] = data[effect] - data['opex'] - data['tax']
    data['icf'] = data['capex'] + data['opex_capital']
    pvi_calculation(data, granula)

    return data


def calc_engine(data, granula, effect_list: list):
    processing_data = data.groupby()
    calculating_objects = processing_data[granula].unique().tolist()

    for granula in calculating_objects:
        processing_data = data.loc[data[granula] == granula, :]

        for effect in effect_list:

            processing_data = basic_calculations(data, effect, granula=granula)
            kpi = kpi_calculations(processing_data, effect, granula=granula)
            func.safe_dataframes_to_excel([data, kpi], ['data', 'kpi'])


if __name__ == '__main__':
    calculation_process()
