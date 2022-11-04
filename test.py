import pandas as pd
import numpy as np
import pyinputplus as pyip
import func
import settings
import mapping as mp
import os
import calculations
from func import timer


# filterwarnings('ignore', category=UserWarning, module='openpyxl')

def process():
    df = pd.DataFrame(5, index=pd.Index(range(100)), columns=['a', 'b'])
    summ(df['a'], df['b'])
    summ(df.a.to_numpy(), df.b.to_numpy())

@timer
def summ(a, b):
    for _ in range(100000):
        c = a + b
    return c


if __name__ == '__main__':
    process()

    print()
