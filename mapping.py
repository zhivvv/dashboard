import os
import pandas as pd
import func
import settings


def decorator_for_mapping_process(run_function):
    @func.timer
    def wrapper():
        print('--------------')
        print('Mapping process')
        print('--------------')
        result = run_function()
        print('Process ended')
        return result

    return wrapper


def decorator_for_save_table(save_function):
    def wrapper(*args):
        print('--------------')
        print('File saving')
        print('--------------')
        return save_function(*args)

    return wrapper


@decorator_for_mapping_process
def mapping_process():
    # Fem files
    fem_results_folder = settings.fem_folder_save
    fem_file_path = os.path.join(fem_results_folder, func.single_input_file(fem_results_folder))
    df = pd.ExcelFile(fem_file_path).parse(settings.fem_sheet_name)
    # Mapping file
    mapping_file = settings.mapping_file_extract
    mapping = pd.ExcelFile(mapping_file)
    mapping = pd.ExcelFile(mapping_file).parse(mapping.sheet_names)

    return Mapping(df, mapping).run().result_mapping


class Mapping:
    columns_to_mapping = ['programme', 'dzo', 'typecf', 'subtypecf']
    result_column_name = 'chosen'

    def __init__(self, df: pd.DataFrame, mapping: dict):
        self._df = df
        self.mapping: dict = mapping
        self.result_mapping: pd.DataFrame = pd.DataFrame()

    def create_mapping_table(self):

        #  | row_number | file_path |   column_name  | value_as_is |           value_to_be          | matched |
        #  ----------------------------------------------------------------------------------------------------
        #  |     55     | /sip_file |   programme    |     ЦИО     | Центр Интегрированных Операций |    1    |

        for column_name in Mapping.columns_to_mapping:
            # Choose mapping table
            mapping_table = self.mapping[column_name].iloc[:, 1:]

            for series_name in mapping_table:
                processing_df = self._df.dropna(subset=[column_name])[column_name]
                res = func.fuzzmatch(input_list=processing_df,
                                     choices=mapping_table[series_name],
                                     show_matched=True,
                                     show_results_in_terminal=False)

                res = func.parse_match_results(res)
                res['column'] = column_name
                self.result_mapping = pd.concat([self.result_mapping, res], axis=0)

        self.result_mapping.reset_index(drop=True, inplace=True)
        return self

    def choose_best_match(self):

        ind_max = self.result_mapping.groupby(['query'])['score'].idxmax()
        self.result_mapping.loc[ind_max, Mapping.result_column_name] = self.result_mapping['result']
        return self

    def best_match_mapping(self):

        for column_name in Mapping.columns_to_mapping:

            column_to_mapping = self.result_mapping[self.result_mapping['column'] == column_name] \
                .dropna(subset=Mapping.result_column_name)[Mapping.result_column_name]
            mapping_table = self.mapping[column_name]
            mapping_column = mapping_table.iloc[:, 0]

            mapping_columns = mapping_table.iloc[:, 1:].columns.to_list()

            for series_name in mapping_columns:
                index_column = mapping_table[series_name]
                series_mapping = pd.Series(data=mapping_column.to_list(),
                                           index=index_column.to_list())
                self.result_mapping['chosen'] = self.result_mapping['chosen'].replace(series_mapping)

        self.result_mapping.dropna(subset=[Mapping.result_column_name], inplace=True)

        return self

    @decorator_for_save_table
    def save_to_mapping(self):

        save_to = settings.mapping_folder_save
        # add columns (file_path)
        func.safe_dataframes_to_excel(dataframes=[self.result_mapping],
                                      sheet_names=['mapping'],
                                      folder_to_save=save_to,
                                      file_name='mapping'
                                      )
        return self

    def run(self):

        (self
         .create_mapping_table()
         .choose_best_match()
         .best_match_mapping()
         .save_to_mapping()
         )

        return self


if __name__ == '__main__':
    mapping_process()
