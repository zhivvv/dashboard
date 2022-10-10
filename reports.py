import pandas as pd
import numpy as np
import os
import func
import settings


def report_process():
    pass

class Reports:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def choose_report(self):
        pass

    def create_full_report(self):
        df['mod_typecf'] = np.where(df['typecf'] == 'costs', df['subtypecf'], df['typecf'])
        df['key'] = df['programme'] + df['mod_typecf']

        programmes = func.groupby_key_field(df, key=['key',
                                                     'programme',
                                                     'mod_typecf',
                                                     'year']
                                            )

        analysis = df.pivot_table(values='value',
                                  index=['key', 'programme', 'mod_typecf'],
                                  columns='year',
                                  aggfunc='sum',
                                  fill_value=0
                                  )
        analysis.reset_index(inplace=True)

        func.safe_dataframes_to_excel([df, programmes, analysis], ['projects', 'programmes', 'analysis'],
                                      # os.path.join(main.base_location, 'fem', 'reports', main.version),
                                      os.path.join(main.base_location, 'tmp'),
                                      # 'programmes_report')
                                      'test')

        return pd.DataFrame

    def programme_report(self):
        return pd.DataFrame

    def save_report(self):
        pass


if __name__ == '__main__':
    report_process()
