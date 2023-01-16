import os
import pandas as pd
import func
import settings


class MappingProcess:

    def __init__(self):
        self.__table_for_mapping = None
        self.__table_mapping = None
        self.__columns = None
        self.result = None

    @staticmethod
    def read_table_from_folder(file_path, sheet_name):
        df = pd.ExcelFile(file_path).parse(sheet_name=sheet_name)
        return df

    def set_table_for_mapping(self, file_path, sheet_name=0):
        if isinstance(file_path, pd.DataFrame):
            object.__table_for_mapping = file_path
        else:
            object.__table_for_mapping = MappingProcess.read_table_from_folder(file_path,
                                                                               sheet_name=sheet_name)
        return self

    def set_table_mapping(self, file_path, sheet_name=0):
        if isinstance(file_path, pd.DataFrame):
            object.__table_mapping = file_path
        else:
            object.__table_mapping = MappingProcess.read_table_from_folder(file_path,
                                                                           sheet_name=sheet_name)
        return self

    def set_columns_to_mapping(self, list_of_columns: list):
        self.__columns = list_of_columns

        return self

    # def mapping_execute(self):
    #     Mapping.create_mapping_table()
    #
    #     return res


@func.process_decorator
def mapping_process():
    extracted_df_file = func.Folder(settings.fem_folder_results).select_file(xls=True)
    extracted_df_path = os.path.join(settings.fem_folder_results, extracted_df_file)
    fem_df = pd.ExcelFile(extracted_df_path).parse()
    mapping_file = pd.ExcelFile(settings.mapping_file_extract)
    mapping_dict = mapping_file.parse(sheet_name=mapping_file.sheet_names)

    result = Mapping(mapping_dict, fem_df).create_mapping_table()

    return result


class Mapping:
    columns_for_mapping = ['programme', 'dzo', 'typecf', 'subtypecf']

    def __init__(self,
                 file_for_mapping: pd.DataFrame,
                 mapping: pd.DataFrame):
        self.file_for_mapping = file_for_mapping
        self.mapping = mapping
        self.result: pd.DataFrame = pd.DataFrame()

    def apply_mapping_to_all_columns(self):

        for col in self.file_for_mapping.columns:
            if col not in self.mapping['name'].unique():
                continue

            tmp_mapping = self.mapping.loc[self.mapping['name'] == col, ['mapping', 'variant']]
            df = func.MatchingProcess(tmp_mapping).mapping_table(query=self.file_for_mapping[col])
            self.result = pd.concat([self.result, df], axis=0)

        return self.result


if __name__ == '__main__':
    mapping_process()
