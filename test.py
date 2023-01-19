import os.path
from mapping import get_mapping_table
import pandas as pd

import func
from func import Folder
import mapping as mp
from func import MatchingProcess

catalog = r'C:\Users\ivanov.ev\Desktop\Dashboard_python'
data_file_name = 'extraction_29112022.xlsx'
mapping_file_name = 'mapping_main.xlsx'
data = pd.read_excel(os.path.join(catalog, data_file_name))
mapping = pd.read_excel(os.path.join(catalog, mapping_file_name))

df = get_mapping_table(data, mapping)
folder = catalog
func.safe_dataframes_to_excel([df], ['mapping'], folder_to_save=folder)

print()
