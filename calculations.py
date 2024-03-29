import dataclasses
import os
import numpy as np
import pandas as pd
import func
import settings
import tqdm
import itertools


class CalculationPrep:

    def __init__(self, data):
        self.data: pd.DataFrame = data
        self.capex = self.__parse_data('capex')
        self.opex = self.__parse_data('opex')
        self.umv = self.__parse_data('umv')
        self.dmv = self.__parse_data('dmv')
        self.npv = self.__parse_data('npv')
        del self.data

    def __parse_data(self, column_name):
        temp = self.data.loc[self.data['typecf'] == column_name, ['year', 'value']]\
            .groupby(by='year').sum().squeeze()
        return temp





@dataclasses.dataclass
class CalcParam:
    base_year = 2022
    rate = 0.14
    rate_past = 0.18
    tax_rate = 0.2
    amort_period = 5
    effect_period = 7

class Calculation:
    def __init__(self, data):

        self.params = CalcParam()
        self.data = data
        # self.base_year = 2022
        # self.rate = 0.14
        # self.rate_past = 0.18
        # self.tax_rate = 0.2
        # self.amort_period = 5
        # self.effect_period = 5

    # before calculation need to consolidate data to date and flows

    def case_calc(self):
        pass

    def batch_calc(self):
        pass




def pivot_typecf(data: pd.DataFrame, column_index: list):
    result = data.pivot_table(values='value',
                              index=column_index,
                              columns='typecf',
                              aggfunc='sum',
                              fill_value=0)

    result = result.reset_index()
    return result


def discount_factor(years: pd.Series, base_year: int,
                    rate: float, rate_past: float = False):
    years = years.drop_duplicates()

    if rate_past:
        disc_factor = years.apply(lambda x: pow((1 + rate_past), (base_year - x - 0.5)) if x < base_year
        else pow((1 + rate), (base_year - x - 0.5))
                                  )
    else:
        disc_factor = years.apply(lambda x: pow((1 + rate), (base_year - x - 0.5)))

    disc_factor.index = years
    return disc_factor


def kpi_calculations(data: pd.DataFrame, granula):
    # add dpp, mirr
    result = data[[granula, 'year', 'cf', 'invest']].copy()
    result['df'] = result['year'].map(discount_factor(result['year'], base_year, rate
                                                      # , rate_past
                                                      ))
    result['cum_dcf'] = result['cf'] * result['df']
    result['pvi'] = result['invest'] * result['df']

    columns = [granula, 'cum_dcf', 'pvi']
    result = result[columns].groupby(granula).sum()
    result['pi'] = result['cum_dcf'] / result['pvi'] + 1
    result = result.reset_index()

    return result


def investment_calculation(data: pd.DataFrame) -> pd.Series:
    accumulated_ocf = data['ocf'].cumsum()
    year_of_min_accumulated_ocf = data.loc[accumulated_ocf.idxmin(), 'year']
    invest = (data['icf'] +
              np.where(
                  (data['year'] <= year_of_min_accumulated_ocf) & (data['ocf'] < 0),
                  -data['ocf'], 0)
              )
    return invest


def check_column_existence(data: pd.DataFrame, columns: list):
    # required_columns = ['capex', 'opex', 'opex_capital', 'tax', 'service', 'effect']
    columns_in_data = data.columns.to_list()
    for column in columns:
        if column not in columns_in_data:
            data[column] = 0
    return data


def basic_calculation(data: pd.DataFrame) -> pd.DataFrame:
    # add effect correction
    # drop fields npv, umv, dmv
    required_columns = ['capex', 'opex', 'opex_capital', 'service', 'umv', 'npv', 'dmv', 'tax']
    check_column_existence(data, required_columns)
    data['effect'] = data['npv'] + data['umv'] + data['dmv']
    data['capex_cut'] = np.where(data['subtypecf'] == 'Cокращение capex', data['effect'], 0)
    data['icf'] = data['capex'] + data['opex_capital']

    # if data['tax'].sum() == 0:
    #     data['tax'] = tax_calculation(data)
    data['cf'] = data['effect'] - (data['capex'] + data['opex'] + data['opex_capital'] +
                                   data['tax'] + data['service'])
    data['ocf'] = data['effect'] - data['capex_cut'] - data['opex'] - data['service'] - data['tax']
    return data


def tax_calculation(data: pd.DataFrame) -> pd.Series:
    amort = amortization_calc(data['icf'])
    ebit = data['effect'] - data['capex_cut'] - data['opex'] - data['service'] - amort
    ebitda = data['effect'] - data['capex_cut'] - data['opex'] - data['service']
    tax = ebit * tax_rate
    return tax


def effects_for_calculation(data: pd.Series):
    data = set(data.unique())
    effects = {'npv', 'umv', 'dmv'}.intersection(data)
    tmp, result = [], []

    for i in range(1, len(effects) + 1):
        combination = itertools.combinations(effects, i)
        for j in combination:
            tmp.append(j)

    for i in tmp:
        if isinstance(i, tuple):
            result.append(list(i))
        else:
            result.append([i])

    return result


def calculation(data, granula):
    costs = ['opex', 'service', 'capex', 'tax', 'opex_capital']
    flows = ['icf', 'ocf', 'cf']
    effects = ['capex_cut', 'effect']
    index = [granula, 'typecf', 'year']
    values = effects + costs + flows
    columns = index + values

    data = data[columns].groupby(index).sum()
    data = data.reset_index()

    result_kpi = pd.DataFrame()
    calculating_objects = data[granula].unique().tolist()

    for case in tqdm.tqdm(calculating_objects):
        processing_case = data.loc[data[granula] == case, :].copy()
        effect_list = effects_for_calculation(processing_case['typecf'])

        for effect in effect_list:
            filter = costs + effect
            processing_data = processing_case.loc[(processing_case['typecf'].isin(filter)), :].copy()
            processing_data['invest'] = investment_calculation(processing_data)
            processing_data['effect_type'] = ", ".join(effect)
            processing_kpi = kpi_calculations(processing_data, granula=granula)
            processing_kpi['effect_type'] = ", ".join(effect)
            result_kpi = pd.concat([result_kpi, processing_kpi], axis=0)

    func.safe_dataframes_to_excel([data, result_kpi], ['data', 'kpi'],
                                  folder_to_save=settings.report_folder_results,
                                  file_name=f'{granula}_report'
                                  )

    return data


def project_calculation(data: pd.DataFrame):
    result_data = pd.DataFrame()
    calculating_objects = data['project'].unique().tolist()

    for case in tqdm.tqdm(calculating_objects):
        processing_case = data.loc[data['project'] == case, :].copy()
        index = data.columns.to_list()
        index.remove('value')
        processing_case = pivot_typecf(processing_case, column_index=index)
        processing_case = basic_calculation(processing_case)
        result_data = pd.concat([result_data, processing_case], axis=0)

    func.safe_dataframes_to_excel([result_data], ['project_calc'],
                                  folder_to_save=settings.calculation_folder_results,
                                  file_name='calculation'
                                  )

    return result_data


def amortization_calc(capex: pd.Series) -> pd.Series:
    amort = []

    def amortization_for_single_year(year, capex):
        years = list(range(year, year + amort_period + 1))
        capex_values = [capex / amort_period if (i > 0)
                                                and (i < amort_period) else
                        capex / amort_period / 2
                        for i in range(amort_period + 1)]

        return pd.Series(capex_values, index=years, name='amortization')

    for idx, value in zip(capex.index, capex):
        amort.append(amortization_for_single_year(idx, value))

    result = pd.concat(amort).groupby(level=0).sum()
    return result


def find_years_for_for_effect(data: pd.DataFrame) -> pd.Series:
    pass


if __name__ == '__main__':
    pass