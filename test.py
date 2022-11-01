import pandas as pd
import numpy as np
import pyinputplus as pyip
import func
import settings
import mapping as mp
import os
import calculations


# filterwarnings('ignore', category=UserWarning, module='openpyxl')

def process():
    fem_folder = settings.report_folder_results
    file_name = func.Folder(fem_folder).select_file()
    fem_path = os.path.join(fem_folder, file_name)
    data = pd.ExcelFile(fem_path).parse()

    calc = calculations.pivot_column(data=data, column_name='typecf', granula='project')
    print()


if __name__ == '__main__':
    process()

    print()
