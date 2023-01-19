import os
import pandas as pd
import func
import settings
from func import MatchingProcess


def create_mapping_table(dict_to_change, mapping, name):
    mapping_table = pd.DataFrame(pd.Series(dict_to_change, name='tmp'))
    res = mapping_table.join(mapping.set_index(name), on='tmp') \
        .reset_index().drop(['tmp'], axis=1)

    return res


def get_mapping_table(data, mapping):
    df = pd.DataFrame()

    for column in data.columns:
        if column not in mapping['name'].unique():
            continue

        tmp_mapping = mapping.loc[mapping['name'] == column, ['mapping', 'variant']]
        res = MatchingProcess(tmp_mapping['variant']).sequence_match(data[column])
        res = create_mapping_table(res, tmp_mapping, 'variant')

        df = pd.concat([df, res], axis=0)

    return df


if __name__ == '__main__':
    pass
