import os.path
from mapping import get_mapping_table, apply_mapping_to_fem
import pandas as pd

import func
from func import Folder
import mapping as mp
from func import MatchingProcess
from calculations import CalculationPrep

# catalog = r''
# data_file_name = 'extraction_29112022.xlsx'
# mapping_file_name = 'mapping_main.xlsx'
# data = pd.read_excel(os.path.join(catalog, data_file_name))
# mapping = pd.read_excel(os.path.join(catalog, mapping_file_name))
#
# df = get_mapping_table(data, mapping)
# folder = catalog
# func.safe_dataframes_to_excel([df], ['mapping'], folder_to_save=folder)


if __name__ == '__main__':

    data = r'/Users/ivanov.ev/Desktop/report30012023.xlsx'
    # df, mapping = map(pd.read_excel, [data_path, mapping_path])
    df = pd.read_excel(data)
    df = df[df['code'] == 'U190001512']

    a = CalculationPrep(df)
    print()

