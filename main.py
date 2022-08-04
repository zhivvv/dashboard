import fem
import os
import pandas as pd

base_location = r'/Users/ivanov.ev/Desktop/Dashboard_python/'
files_location = 'ФЭМ/for_load'
sheet_name = 'Основной лист'

if __name__ == '__main__':

    df = None
    fem_folder = os.path.join(base_location, files_location)
    file_list = os.listdir(fem_folder)

    for filename in file_list:
        try:
            tmp_df = fem.extract_fem_from_excel_file(os.path.join(fem_folder, filename), sheet_name=sheet_name)
            # tmp_df = fem.melt_year_column(tmp_df)
            # tmp_df = fem.apply_unit_to_value(tmp_df)

        except IOError:
            print('IOError error raised. This error is acceptable')

        if df is None:
            df = tmp_df
        else:
            df = pd.concat([df, tmp_df], axis=0)
    #
    # df.reset_index(inplace=True, drop=True)
    # df = fem.unstack_column(df,'Подтип CF (выбрать из списка)')
    # df = fem.flatten_columns(df)
    # df = df.sort_values(by=['Программа (ИСУП)', 'Название проекта (ИСУП)', 'Тип CF (выбрать из списка)', 'Год'])
    # df = fem.add_columns(df)
    #
    # df = fem.fem(df)
    # fem.save_file(df, file_name='test', file_type='fem')

    #
    print('end')
