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
        # get rid of names in columns. TODO
        # Use only index of column, because we know that there are only 3 columns in mapping file
        tmp_mapping = mapping.loc[mapping['column_name'] == column, ['mapping', 'variant']]
        res = MatchingProcess(tmp_mapping['variant']).sequence_match(data[column])
        res = create_mapping_table(res, tmp_mapping, 'variant')
        res['column_name'] = column

        df = pd.concat([df, res], axis=0)

    df.rename(columns={'index': 'value'}, inplace=True)
    # df.drop('index', axis=1, inplace=True)

    return df


def apply_mapping_to_fem(fem: pd.DataFrame, mapping: pd.DataFrame, fillna=True):
    result = fem.copy(deep=True)
    columns_in_mapping = mapping['column_name'].unique().tolist()
    mapping_column_names = ['value', 'mapping']

    for fem_column in fem.columns:
        if fem_column in columns_in_mapping:
            temp_mapping = mapping.loc[mapping['column_name'] == fem_column,
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
