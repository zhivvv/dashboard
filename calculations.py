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
        df['OCF_new'] = - direct_effect_filter * df['Сокращение CAPEX']
    return df

def calculations(df: pd.DataFrame):
    df['Затраты'] = df['CAPEX'] + df['OPEX']
    a_index = df['OCF'].cumsum().argmin()
    return sum(df['OPEX'].iloc[0:a_index + 1])
