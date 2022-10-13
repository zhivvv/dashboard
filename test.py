import pandas as pd
import numpy as np
import pyinputplus as pyip
import func
import settings


# filterwarnings('ignore', category=UserWarning, module='openpyxl')

def process():
    # mapping = ['гонка', 'горак', 'загореть']
    # mapping = pd.Series(data=mapping, name='a')
    # query = 'гора'
    #
    # a = func.MatchingProcess(mapping).single_match(query=query,
    #                                                show_results_in_terminal=True
    #                                                )
    #
    # mapping = ['гонка', 'горак', 'загореть']
    # mapping = pd.Series(data=mapping, name='a')
    # query = ['гора', 'горн']
    # query = pd.Series(data=query, name='query')
    #
    # b = func.MatchingProcess(mapping).sequence_match(query=query,
    #                                                  show_results_in_terminal=True
    #                                                  )

    mapping = pd.DataFrame({'a': ['гонка', 'горак', 'загореть'],
                            'b': ['гон', 'рак', 'реветь']
                            })
    query = ['гора', 'горн']
    query = pd.Series(data=query, name='query')

    c = func.MatchingProcess(mapping).best_sequence_match(query=query,
                                                          show_results_in_terminal=True,
                                                          drop_not_best=False
                                                          )

    # print(a)
    # print(b)
    print(c)


if __name__ == '__main__':
    process()

    print()
