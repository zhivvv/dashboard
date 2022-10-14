import os
import pandas as pd
import func
import settings


@func.process_decorator
def mapping_process():
    columns_for_mapping = ['programme', 'dzo', 'typecf', 'subtypecf']

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
                 mapping_file: dict,
                 df_mapping: pd.DataFrame):
        self.mapping_dict = mapping_file
        self.df = df_mapping
        self.result: pd.DataFrame = pd.DataFrame()

    def create_mapping_table(self):
        for column_name in Mapping.columns_for_mapping:
            mapping_table = self.mapping_dict[column_name]
            temp = func.MatchingProcess(mapping_table).mapping_table(self.df[column_name])
            self.result = pd.concat([self.result, temp], axis=0)

        func.safe_dataframes_to_excel(dataframes=[self.result],
                                      sheet_names=[settings.mapping_sheet_name],
                                      folder_to_save=settings.mapping_folder_results,
                                      file_name='mapping')

        return self.result


if __name__ == '__main__':
    mapping_process()
