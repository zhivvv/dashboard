import os
import numpy as np
import pandas as pd
import func
import settings
import tqdm
import itertools

# get data from file

base_year = 2022
rate = 0.14
rate_past = 0.18
tax_rate = 0.2
amort_period = 5
effect_period = 5


class CalculationPrep:

    # data format
    # index (year or month) | effect | capex | opex | service |
    # add data check and write tests
    def __init__(self, data):
        self.data = data


class Calculation:
    def __init__(self, data):
        self.data = data

    def case_calc(self):
        pass

    def batch_calc(self):
        pass


class BatchProcessing(CalculationPrep):
    def __init__(self):
        super(BatchProcessing, self).__init__()


# todo move to another module
def choose_excel_file(folder_path, sheet_name=0):
    file_path = os.path.join(folder_path, func.single_input_file(folder_path))
    result = pd.ExcelFile(file_path).parse(sheet_name)
    return result


# todo move to another module
def apply_mapping_to_fem(fillna=True):
    fem: pd.DataFrame = choose_excel_file(settings.fem_folder_results,
                                          sheet_name=settings.fem_sheet_name)
    mapping: pd.DataFrame = choose_excel_file(settings.mapping_folder_results,
                                              sheet_name=settings.mapping_sheet_name)

    result = fem.copy(deep=True)

    columns_in_mapping = mapping.column.unique().tolist()
    mapping_column_names = ['query', 'chosen']

    for fem_column in fem.columns:
        if fem_column in columns_in_mapping:
            temp_mapping = mapping.loc[mapping['column'] == fem_column,
                                       mapping_column_names].copy()

            temp_dict = (temp_mapping
                         .set_index(mapping_column_names[0])[mapping_column_names[1]]
                         .to_dict()
                         )

            if fillna:
                result[fem_column] = (result[fem_column]
                                      .map(temp_dict)
                                      .fillna(result[fem_column])
                                      )
            else:
                result[fem_column] = result[fem_column].map(temp_dict)

        result.fillna('n/a', inplace=True)

    return result


def move_costs_to_typecf(fem: pd.DataFrame):
    fem['typecf'] = np.where(fem['typecf'] == 'Затраты', fem['subtypecf'],
                             fem['typecf'])

    return fem


def calculation_process():
    # load data
    fem = apply_mapping_to_fem(fillna=True)
    fem = move_costs_to_typecf(fem)

    return project_calculation(fem)


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
    calculation_process()
