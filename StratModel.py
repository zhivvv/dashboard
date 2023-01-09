import pandas as pd
import func

FILE_PATH = "/Users/ivanov.ev/Desktop/2022_07_29_Выгрузка_СМ_короткая.xlsx"


def file_loading(path):

    sh = pd.ExcelFile(path).sheet_names
    print(sh)
    df = pd.ExcelFile(path).parse()
    print()
    return df



if __name__ == '__main__':
    data = file_loading(FILE_PATH)
    print()