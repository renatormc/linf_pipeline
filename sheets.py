from dataclasses import dataclass
import pandas as pd
import random


@dataclass
class RandomObjeto:
    tipo: str
    subtipo: str


class Random:
    def __init__(self) -> None:
        xls = pd.ExcelFile('dados.xlsx')

        df_stat_qtd_objetos = pd.read_excel(xls, 'estatistica_qtd_objetos')
        self.values_qtd_objetos = list(df_stat_qtd_objetos['Qtd objetos'])
        total = df_stat_qtd_objetos['Quantidade'].sum()
        self.probabilites_qtd_objetos = list(map(lambda x: x/total, list(df_stat_qtd_objetos['Quantidade'])))

        df_stat_tipo_objeto = pd.read_excel(xls, 'estatistica_tipo_objeto')
        self.values_tipo_objeto = list(df_stat_tipo_objeto['Tipo'])
        total = df_stat_tipo_objeto['Quantidade'].sum()
        self.probabilites_tipo_objeto = list(map(lambda x: x/total, list(df_stat_tipo_objeto['Quantidade'])))

        df_stat_tipo_extracao = pd.read_excel(xls, 'estatistica_celular')
        self.values_tipo_extracao = list(df_stat_tipo_extracao['Tipo'])
        total = df_stat_tipo_extracao['Quantidade'].sum()
        self.probabilites_tipo_extracao = list(map(lambda x: x/total, list(df_stat_tipo_extracao['Quantidade'])))

        df_stat_capacidade_computador = pd.read_excel(xls, 'estatistica_computador')
        self.values_capacidade_computador = list(df_stat_capacidade_computador['Capacidade'])
        total = df_stat_capacidade_computador['Quantidade'].sum()
        self.probabilites_capacidade_computador = list(map(lambda x: x/total, list(df_stat_capacidade_computador['Quantidade'])))

    def gerar_qtd_objetos(self) -> int:
        return random.choices(self.values_qtd_objetos, self.probabilites_qtd_objetos)[0]

    def gerar_tipo_objeto(self) -> str:
        return random.choices(self.values_tipo_objeto, self.probabilites_tipo_objeto)[0]

    def gerar_tipo_extracao(self) -> str:
        return random.choices(self.values_tipo_extracao, self.probabilites_tipo_extracao)[0]

    def gerar_capacidade_computador(self) -> str:
        return random.choices(self.values_capacidade_computador, self.probabilites_capacidade_computador)[0]

    def gerar_objeto(self) -> RandomObjeto:
        tipo = self.gerar_tipo_objeto()
        subtipo = self.gerar_capacidade_computador() if tipo == "Computador" else self.gerar_tipo_extracao()
        return RandomObjeto(tipo=tipo, subtipo=subtipo)


rd = Random()
for i in range(100):
    print(f"\nGerando perícia {i}")
    for j in range(rd.gerar_qtd_objetos()):
        print(rd.gerar_objeto())
