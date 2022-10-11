import pandas as pd
import numpy as np
import os
import func
import settings
import pyinputplus as pyip


def decorator_for_report_process(run_function):
    @func.timer
    def wrapper():
        print('--------------')
        print('Report process')
        print('--------------')
        result = run_function()
        print('Process ended')
        return result

    return wrapper


@decorator_for_report_process
def report_process():
    return (Reports(fem_folder_results=settings.fem_folder_results,
                    mapping_folder_results=settings.mapping_folder_results)
            .run()
            )


def choose_excel_file(folder_path, sheet_name=0):
    file_path = os.path.join(folder_path, func.single_input_file(folder_path))
    result = pd.ExcelFile(file_path).parse(sheet_name)
    return result


class Reports:

    def __init__(self, fem_folder_results, mapping_folder_results):

        self.fem: pd.DataFrame = choose_excel_file(fem_folder_results, sheet_name=settings.fem_sheet_name)
        self.mapping: pd.DataFrame = choose_excel_file(mapping_folder_results,
                                                       sheet_name=settings.mapping_sheet_name)
        self.result = self.fem.copy(deep=True)
        self.user_choice: str | int | None = None
        self.report_dict = {'full_report': self.full_report,
                            'programme_report': self.programme_report
                            }

    def select_report(self):

        print('--------------')
        print('Reports: ')
        print('--------------')

        # Choose option
        for i in enumerate(self.report_dict):
            print(i[0] + 1, ' - ', i[1], sep='')

        report_number = pyip.inputNum(prompt='Report: ',
                                      min=1,
                                      max=len(self.report_dict)
                                      )

        self.user_choice = list(self.report_dict)[report_number - 1]
        print(self.user_choice)

        return self.user_choice

    def apply_mapping_to_fem(self, fillna=True):
        mapping_column_names = ['query', 'chosen']
        columns_in_mapping = self.mapping.column.unique().tolist()

        for fem_column in self.fem.columns:
            if fem_column in columns_in_mapping:
                temp_mapping = self.mapping.loc[self.mapping['column'] == fem_column,
                                                mapping_column_names].copy()

                temp_dict = (temp_mapping
                             .set_index(mapping_column_names[0])[mapping_column_names[1]]
                             .to_dict()
                             )

                if fillna:
                    self.result[fem_column] = (self.result[fem_column]
                                               .map(temp_dict)
                                               .fillna(self.result[fem_column])
                                               )
                else:
                    self.result[fem_column] = self.result[fem_column].map(temp_dict)

        return self

    def full_report(self):
        report_name = 'full_report'

        self.apply_mapping_to_fem(fillna=True)

        self.result['typecf'] = np.where(self.result['typecf'] == 'Затраты', self.result['subtypecf'],
                                         self.result['typecf'])

        func.safe_dataframes_to_excel(dataframes=[self.result],
                                      sheet_names=[report_name],
                                      folder_to_save=settings.report_folder_results,
                                      file_name=report_name
                                      )

        return self.result

    def programme_report(self):
        programmes = func.groupby_key_field(self.fem,
                                            key=['key',
                                                 'programme',
                                                 'mod_typecf',
                                                 'year']
                                            )

        analysis = self.fem.pivot_table(values='value',
                                        index=['key', 'programme', 'mod_typecf'],
                                        columns='year',
                                        aggfunc='sum',
                                        fill_value=0
                                        )
        analysis.reset_index(inplace=True)

        return self.result

    def run(self):

        self.report_dict[self.select_report()]()

        return self


if __name__ == '__main__':
    report_process()
