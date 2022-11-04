import os
import numpy as np
import pandas as pd
import pyinputplus as pyip
import func
import settings
import tqdm

base_year = 2020
rate = 0.14


def calculation_process():
    # load data
    file_folder = settings.report_folder_results
    file_name = 'full_report_02112022.xlsx'
    df = pd.ExcelFile(os.path.join(file_folder, file_name)).parse()

    # project = 'Openbox'
    granula = 'project'
    column_to_unstack = 'typecf'
    effect = ['npv', 'umv', 'dmv']

    data = pivot(data=df, column_name=column_to_unstack, granula=granula)

    result = calc_cases(data, granula, effect)

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

    result = data[[granula, 'year', 'cf', 'invest']].copy()
    result['df'] = result['year'].apply(lambda x: pow((1 + rate), (base_year - x - 0.5)))
    result['dcf'] = result['cf'] * result['df']
    result['pvi'] = result['invest'] * result['df']
    result = result[[granula, 'dcf', 'pvi']].groupby(granula).sum()

    result['pi'] = result['dcf'] / result['pvi'] + 1

    rename_dict = {'dcf': effect}
    result = result.reset_index().rename(columns=rename_dict)

    return result


def investment_calculation(data: pd.DataFrame, granula):
    data['aocf'] = data[[granula, 'ocf']].groupby(granula).cumsum()
    data['year_min_aocf'] = data.loc[data['aocf'].idxmin(), 'year']

    data['invest'] = (data['capex'] + data['opex_capital'] +
                   np.where(
                       (data['year'] <= data['year_min_aocf'])
                       & (data['ocf'] < 0),
                       -data['ocf'], 0
                   )
                   )
    return data


def basic_calculations(data: pd.DataFrame, effect: str, granula):
    data['costs'] = (data['capex'] + data['opex'] + data['opex_capital']
                     + data['tax'] + data['service'])
    data['cf'] = data[effect] - data['costs']
    # data['df'] = data['year'].apply(lambda x: pow((1 + rate), (base_year - x - 0.5)))
    # data['dcf'] = data['cf'] * data['df']
    data['ocf'] = data[effect] - data['opex'] - data['service'] - data['tax']
    data['icf'] = data['capex'] + data['opex_capital']
    investment_calculation(data, granula)

    return data


def calc_cases(data, granula, effect_list: list):
    # processing_data = data.groupby()
    calculating_objects = data[granula].unique().tolist()
    amount = len(calculating_objects)

    result_data = pd.DataFrame()
    result_kpi = pd.DataFrame()

    for case in tqdm.tqdm(calculating_objects):
        processing_data = data.loc[data[granula] == case, :].copy()

        for effect in effect_list:
            processing_data = basic_calculations(processing_data, effect, granula=granula)
            processing_data['effect'] = effect
            processing_kpi = kpi_calculations(processing_data, effect, granula=granula)
            result_data = pd.concat([result_data, processing_data], axis=0)
            result_kpi = pd.concat([result_kpi, processing_kpi], axis=0)

    func.safe_dataframes_to_excel([result_data, result_kpi], ['data', 'kpi'],
                                  folder_to_save=settings.calculation_folder_results,
                                  file_name='calculation'
                                  )

    return


if __name__ == '__main__':
    calculation_process()
