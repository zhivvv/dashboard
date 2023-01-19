import pandas as pd
import mapping as mp
from func import MatchingProcess

path = r"C:\Users\ivanov.ev\Desktop\test.xlsx"
df = pd.read_excel(path, sheet_name='data')
mapping = pd.read_excel(path, sheet_name='МК')
mapping = mapping.dropna(axis=0)

# choices = mapping.iloc[:, 0].copy()

choices = ['aaa', 'bbb', 'ccc']
# query = ['a', 'b', 'c']
query = 'a'
res = MatchingProcess(choices).single_match(query, get_score=False)
# res = MatchingProcess(choices).sequence_match(query)
print()