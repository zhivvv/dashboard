import os
import pandas as pd
from func import MatchingProcess


def create_mapping_table(dict_to_change, mapping, name):
    mapping_table = pd.DataFrame(pd.Series(dict_to_change, name='tmp'))
    res = mapping_table.join(mapping.set_index(name), on='tmp') \
        .reset_index().drop(['tmp'], axis=1)

    return res


def get_mapping_table(data: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()

    for column in data.columns:
        if column not in mapping['column_name'].unique():
            continue

        tmp_mapping = mapping.loc[mapping['column_name'] == column, ['mapping', 'variant']]
        res = MatchingProcess(tmp_mapping['variant']).sequence_match(data[column])
        res = create_mapping_table(res, tmp_mapping, 'variant')

        df = pd.concat([df, res], axis=0)

    return df


# def choose_excel_file(folder_path, sheet_name=0):
#     file_path = os.path.join(folder_path, func.single_input_file(folder_path))
#     result = pd.ExcelFile(file_path).parse(sheet_name)
#     return result


def apply_mapping_to_fem(fem: pd.DataFrame, mapping: pd.DataFrame, fillna=True):
    # fem: pd.DataFrame = choose_excel_file(settings.fem_folder_results,
    #                                       sheet_name=settings.fem_sheet_name)
    # mapping: pd.DataFrame = choose_excel_file(settings.mapping_folder_results,
    #                                           sheet_name=settings.mapping_sheet_name)

    result = fem.copy(deep=True)

    columns_in_mapping = mapping.column.unique().tolist()
    mapping_column_names = ['query', 'chosen']

    for fem_column in fem.columns:
        if fem_column in columns_in_mapping:
            temp_mapping = mapping.loc[mapping['column'] == fem_column,
                                       mapping_column_names].copy()

            temp_dict = (temp_mapping
                         .set_index(mapping_column_names[0])[mapping_column_names[1]]
                         .to_dict()
                         )

            if fillna:
                result[fem_column] = (result[fem_column]
                                      .map(temp_dict)
                                      .fillna(result[fem_column])
                                      )
            else:
                result[fem_column] = result[fem_column].map(temp_dict)

        result.fillna('n/a', inplace=True)

    return result


if __name__ == '__main__':
    pass
