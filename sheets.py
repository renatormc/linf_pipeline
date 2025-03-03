from dataclasses import dataclass
from datetime import timedelta
import pandas as pd
import random


@dataclass
class TarefaData:
    objeto: str
    subtipo: str
    tarefa: str
    duracao: timedelta
    recursos: list[str]


@dataclass
class RecursoData:
    nome: str
    quantidade: int


class Planilha:
    def __init__(self) -> None:
        xls = pd.ExcelFile('dados.xlsx')

        df_stat_qtd_objetos = pd.read_excel(xls, 'estatistica_qtd_objetos')
        df_stat_qtd_objetos.columns = df_stat_qtd_objetos.columns.str.strip()
        self.values_qtd_objetos = list(df_stat_qtd_objetos['Qtd objetos'])
        total = df_stat_qtd_objetos['Quantidade'].sum()
        self.probabilites_qtd_objetos = list(map(lambda x: x/total, list(df_stat_qtd_objetos['Quantidade'])))

        df_stat_tipo_objeto = pd.read_excel(xls, 'estatistica_tipo')
        df_stat_tipo_objeto.columns = df_stat_tipo_objeto.columns.str.strip()
        self.values_tipo_objeto = list(df_stat_tipo_objeto['Tipo'])
        total = df_stat_tipo_objeto['Quantidade'].sum()
        self.probabilites_tipo_objeto = list(map(lambda x: x/total, list(df_stat_tipo_objeto['Quantidade'])))

        df = pd.read_excel(xls, 'estatistica_subtipo')
        df.columns = df.columns.str.strip()

        self.values_subtipo: dict[str, list[str]] = {}
        self.probabilidades_subtipo: dict[str, list[float]] = {}
        for _, row in df_stat_tipo_objeto.iterrows():
            tipo = row['Tipo']
            df2 = df[df['Objeto'] == tipo]
            self.values_subtipo[tipo] = list(df2['Subtipo'])
            total = df2['Quantidade'].sum()
            self.probabilidades_subtipo[tipo] = list(map(lambda x: x/total, list(df2['Quantidade'])))

        self.df_tarefas = pd.read_excel(xls, 'tarefas')
        self.df_tarefas['Recurso 1'] = self.df_tarefas['Recurso 1'].fillna('')
        self.df_tarefas['Recurso 2'] = self.df_tarefas['Recurso 2'].fillna('')
        self.df_tarefas['Recurso 3'] = self.df_tarefas['Recurso 3'].fillna('')
        self.df_tarefas['Recurso 4'] = self.df_tarefas['Recurso 4'].fillna('')
        self.df_tarefas.columns = self.df_tarefas.columns.str.strip()

        self.df_recursos = pd.read_excel(xls, 'recursos')
        self.df_recursos.columns = self.df_recursos.columns.str.strip()

    def gerar_qtd_objetos(self) -> int:
        return random.choices(self.values_qtd_objetos, self.probabilites_qtd_objetos)[0]

    def gerar_tipo_objeto(self) -> str:
        return random.choices(self.values_tipo_objeto, self.probabilites_tipo_objeto)[0]

    def gerar_subtipo_objeto(self, tipo: str) -> str:
        return random.choices(self.values_subtipo[tipo], self.probabilidades_subtipo[tipo])[0]

    def extract_tarefa(self, row: pd.Series) -> TarefaData:
        reclist: list[str] = [row['Recurso 1'].strip(), row['Recurso 2'].strip(), row['Recurso 3'].strip(), row['Recurso 4'].strip()]
        return TarefaData(
            row['Objeto'],
            row['Subtipo'],
            row['Tarefa'],
            timedelta(
                hours=row['Duração'].hour,
                minutes=row['Duração'].minute,
                seconds=row['Duração'].second,
                microseconds=row['Duração'].microsecond
            ),
            [rec for rec in reclist if rec != '']
        )

    def get_recursos(self) -> list[RecursoData]:
        return [RecursoData(row['Nome'], row['Quantidade']) for _, row in self.df_recursos.iterrows()]

    def get_peritos(self) -> list[str]:
        df2 = self.df_recursos[self.df_recursos['Nome'] == 'Perito']
        if df2.empty:
            raise Exception('Não há peritos disponíveis')
        qtd = df2.loc[0, 'Quantidade']
        assert isinstance(qtd, int)
        return [f'Perito {i + 1}' for i in range(qtd)]
        
    def get_tarefas(self, objeto: str, subtipo: str) -> list[TarefaData]:
        df = self.df_tarefas[(self.df_tarefas['Objeto'] == objeto) & (self.df_tarefas['Subtipo'] == subtipo)]
        return [self.extract_tarefa(row) for _, row in df.iterrows()]
