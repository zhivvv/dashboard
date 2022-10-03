import pandas as pd
import numpy as np
import main
import os
import func


if __name__ == '__main__':

    path_to_folder = os.path.join(main.base_location, 'fem', 'processing', main.version)

    df = func.select_table_to_filelist(folder_path_to_list=path_to_folder, sheet_name=main.sheet_name)

    # Report 1 - programmes

    df['mod_typecf'] = np.where(df['typecf'] == 'costs', df['subtypecf'], df['typecf'])
    df['key'] = df['programme'] + df['mod_typecf']

    programmes = func.groupby_key_field(df, key=['key',
                                                 'programme',
                                                 'mod_typecf',
                                                 'year']
                                        )

    analysis = df.pivot_table(values='value',
                              index=['key', 'programme', 'mod_typecf'],
                              columns='year',
                              aggfunc='sum',
                              fill_value=0
                              )
    analysis.reset_index(inplace=True)

    func.safe_dataframes_to_excel([df, programmes, analysis], ['projects', 'programmes', 'analysis'],
                                  # os.path.join(main.base_location, 'fem', 'reports', main.version),
                                  os.path.join(main.base_location, 'tmp'),
                                 # 'programmes_report')
                                 'test')

