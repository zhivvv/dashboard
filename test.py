import pandas as pd
import numpy as np
import pyinputplus as pyip
import func
import settings
import mapping as mp
import os

# filterwarnings('ignore', category=UserWarning, module='openpyxl')

def process():

    columns_for_mapping = ['programme', 'dzo', 'typecf', 'subtypecf']

    extracted_df_file = func.Folder(settings.fem_folder_results).select_file(xls=True)
    extracted_df_path = os.path.join(settings.fem_folder_results, extracted_df_file)
    extracted_df = pd.ExcelFile(extracted_df_path).parse()
    mapping_file = pd.ExcelFile(settings.mapping_file_extract)
    mapping_dict = mapping_file.parse(sheet_name=mapping_file.sheet_names)

    for column_name in columns_for_mapping:
        mapping_table = mapping_dict[column_name]
        temp = func.MatchingProcess(mapping_table).mapping_table(extracted_df[column_name])



if __name__ == '__main__':
    process()

    print()
