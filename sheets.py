import pandas as pd
import random

class Random:
    def __init__(self) -> None:
        self.stat = {1: 50, 2: 45, 3: 35, 4: 25, 5: 15, 6: 10, 7: 2}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = list(map(lambda x: x/total, self.stat.values()))


    def random[T](self, df: pd.DataFrame, col_values: str, col_qtds: str) -> T:
        values = list(df[col_values])
        total = df[col_qtds].sum()
        df['Probabilidade'] = df[col_qtds].apply(lambda x: x/total)
        probabilites = list(map(lambda x: x/total, list(df[col_qtds])))
        return  random.choices(values, probabilites)[0]



xls = pd.ExcelFile('dados.xlsx')
df_stat_qtd_objetos = pd.read_excel(xls, 'estatistica_qtd_objetos')
rd = Random()
print(rd.random[int](df_stat_qtd_objetos, "Qtd objetos", "Quantidade"))

