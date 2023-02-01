import pandas as pd

path = 'atlas.xlsx'
sheets = ['Функционал', 'Процессы', 'Операции', 'Эффект', 'Роли', 'ДО']
data = dict()
file = pd.ExcelFile(path)
for i in sheets:
    data[i]: pd.DataFrame = file.parse(i)

df = data['Процессы'] \
    .set_index('%id process') \
    .join(data['Операции']
          .set_index('%id process')
          )

print()

if __name__ == '__main__':
    pass
