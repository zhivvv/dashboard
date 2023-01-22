import os.path
from mapping import get_mapping_table, apply_mapping_to_fem
import pandas as pd

import func
from func import Folder
import mapping as mp
from func import MatchingProcess

# catalog = r''
# data_file_name = 'extraction_29112022.xlsx'
# mapping_file_name = 'mapping_main.xlsx'
# data = pd.read_excel(os.path.join(catalog, data_file_name))
# mapping = pd.read_excel(os.path.join(catalog, mapping_file_name))
#
# df = get_mapping_table(data, mapping)
# folder = catalog
# func.safe_dataframes_to_excel([df], ['mapping'], folder_to_save=folder)

print()

if __name__ == '__main__':
    mapping_path = r'/Users/ivanov.ev/Desktop/mapping.xlsx'
    data_path = r'/Users/ivanov.ev/Desktop/extraction21012023.xlsx'
    df, mapping = map(pd.read_excel, [data_path, mapping_path])

    path_to_save = '/Users/ivanov.ev/Desktop'
    file_name = 'map.xlsx'
    a = get_mapping_table(df, mapping)
    # a.to_excel(excel_writer=os.path.join(path_to_save, file_name),
    #            sheet_name='a',
    #            index=False)
    b = apply_mapping_to_fem(df, a)

    print()
