import pandas as pd
import numpy as np

PATH = r'it_masterbook.xlsx'


class ITMasterBookParser:

    def __init__(self, data_path):
        self.sheet_name = 'mk'
        self.rawdata = pd.read_excel(data_path, sheet_name=self.sheet_name)
        self.__case_attr()
        self.__get_data()

        del self.sheet_name
        del self.rawdata

    def __case_attr(self):
        temp = self.rawdata.T.reset_index()
        user_attr = temp.iloc[0:2, 0:6]
        user_attr.columns = user_attr.iloc[0]
        user_attr = user_attr.iloc[1]

        self.code = user_attr[0]
        self.project_name = user_attr[1]
        self.programme = user_attr[2]
        self.start_date = user_attr[3]
        self.version = user_attr[4]
        self.made_by = user_attr[5]

    def __get_data(self):
        df = self.rawdata.iloc[6:]
        # self.rawdata
        self.data = df

    def prepare_for_calculation(self):
        pass



if __name__ == '__main__':
    case = ITMasterBookParser(PATH)

    print()
