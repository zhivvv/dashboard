import pandas as pd
from datetime import datetime
import math


def find_functionality_use_in_first_year(iterations: pd.Series,
                                         prod_date: pd.Series):
    def find_years_in_year(date: pd.Timestamp):
        first_day_of_year = datetime(date.year, 1, 1)
        last_day_of_year = datetime(date.year, 12, 31)

        return (last_day_of_year - first_day_of_year).days + 1

    def days_from_year_start(date: pd.Timestamp):
        first_day_of_year = datetime(date.year, 1, 1)

        return (date - first_day_of_year).days + 1

    # check_dates()

    days_from_start = prod_date.apply(days_from_year_start)
    interval = prod_date.apply(find_years_in_year) / iterations
    result = days_from_start / interval
    result.apply(math.ceil)

    return result


def parse_info():
    pass


def get_average_hour_rate(month_rate):
    months_in_year = 12
    year_work_days = 247
    day_work_hours = 8
    social_payments = 0.3
    hour_rate = (month_rate *
                 (1 + social_payments) *
                 months_in_year /
                 year_work_days /
                 day_work_hours
                 )

    return hour_rate


def report(data: dict):
    right_columns = {
        'Эффект': ['%id func', '%id oper', 'Эффект'],
        'Операции': ['%id oper', '%id process', '%id role',
                     'Название операции', 'AS IS, часов'],
        'Функционал': ['%id func', 'Название функционала',
                       'Раздел', 'Дата выхода в прод',
                       'Стоимость разработки, тыс. руб.'],
        'Процессы': ['%id process', 'Название процесса',
                     'Номер в каталоге', 'Итераций в год'],
        'Роли': ['%id role', 'Роль'],
        'Люди': ['%id oper', '%id do', 'Кол-во человек'],
        'ДО': ['%id do', 'ДО', 'Ср. ставка, тыс. руб. в мес.']
    }

    ops = (
        data['Операции'][right_columns['Операции']]
        .merge(
            data['Процессы'][right_columns['Процессы']],
            how='outer', on='%id process'
        )
        .merge(
            data['Эффект'][right_columns['Эффект']]
            .groupby(by='%id oper').sum(['Эффект']),
            how='outer', on='%id oper'
        )
        .merge(
            data['Роли'][right_columns['Роли']],
            how='outer', on='%id role'
        )
        .merge(
            data['Люди'][right_columns['Люди']],
            how='outer', on='%id oper'
        )
        .merge(
            data['ДО'][right_columns['ДО']],
            how='outer', on='%id do'
        )
    )

    # ops.loc[:, '#TO BE, часов'] = ops['#AS IS, часов'] * (1 - ops['Эффект'])
    # ops.loc[:, '#Экономия, часов'] = ops['#AS IS, часов'] - ops['#TO BE, часов']
    ops['Ср. ставка, тыс. руб. в час'] = (
        ops['Ср. ставка, тыс. руб. в мес.']
        .apply(get_average_hour_rate)
    )

    ops['TO BE, часов'] = (
        ops['AS IS, часов'] *
        (1 - ops['Эффект'])
    )

    ops['Эффект, часов'] = (
        ops['AS IS, часов'] *
        ops['Эффект']
    )

    ops['Эффект, тыс. руб. в год'] = (
        ops['Эффект, часов'] *
        ops['Ср. ставка, тыс. руб. в час'] *
        ops['Кол-во человек'] *
        ops['Итераций в год']
    )

    return ops


path = 'atlas.xlsx'
sheets = ['Функционал', 'Процессы', 'Операции',
          'Эффект', 'Роли', 'ДО', 'Люди', 'info']
data = dict()
file = pd.ExcelFile(path)
for i in sheets:
    data[i]: pd.DataFrame = file.parse(i)

# res = process_report(data)
res: pd.DataFrame = report(data)
res.to_excel('result.xlsx', sheet_name='result', index=False)
print()

if __name__ == '__main__':
    pass
