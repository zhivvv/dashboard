import fem
import os
import pandas as pd

base_location = 'path_to_dashboard'
files_location = r'/Users/ivanov.ev/Desktop/ФЭМ'
sheet_name = 'Основной лист'

if __name__ == '__main__':

    file_list = []
    df = None

    for filename in os.listdir(files_location):
        list_of_possible_extensions_for_pandas = ['.xlsx', '.xls', '.xlsm', '.xlsb']
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in list_of_possible_extensions_for_pandas:
            continue
        file_loc = os.path.join(files_location, filename)

        tmp_df = fem.extract_fem_from_excel_file(file_loc, sheet_name=sheet_name)
        tmp_df = fem.melt_year_column(tmp_df)
        tmp_df = fem.apply_unit_to_value(tmp_df)

        if df is not None:
            df = pd.concat([df, tmp_df], axis=0)
        else:
            df = tmp_df

    df.reset_index(inplace=True, drop=True)
    df = fem.unstack_column(df,'Подтип CF (выбрать из списка)')
    df = fem.flatten_columns(df)
    df = df.sort_values(by=['Программа (ИСУП)', 'Название проекта (ИСУП)', 'Тип CF (выбрать из списка)', 'Год'])
    df = fem.add_columns(df)

    df = fem.fem(df)
    # fem.save_file(df, file_name='test', file_type='fem')

    #
    print()
