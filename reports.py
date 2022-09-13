import pandas as pd
import numpy as np
import main
import os
import fem




path_to_folder = os.path.join(main.base_location, 'fem', 'processing', main.version)

df = fem.select_table_to_filelist(folder_path_to_list=path_to_folder, sheet_name=main.sheet_name)
df['mod_typecf'] = np.where(df['typecf'] == 'costs', df['subtypecf'], df['typecf'])
df['key'] = df['programme'] + df['mod_typecf']
programmes = fem.groupby_key_field(df, key=['key', 'programme', 'typecf', 'subtypecf', 'year', 'mod_typecf'])

economy = programmes[programmes['programme'] == 'ЦЭк']

analysis = df.pivot_table(values='value',
                          index=['key', 'programme', 'mod_typecf'],
                          columns='year',
                          aggfunc='sum',
                          )
analysis.reset_index(inplace=True)

fem.safe_dataframes_to_excel([programmes, analysis], ['programmes', 'analysis'],
                             os.path.join(main.base_location, 'fem', 'reports', main.version),
                             'programmes_report')



print()