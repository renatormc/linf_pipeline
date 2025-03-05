from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
import pandas as pd
import random


@dataclass
class EtapaData:
    objeto: str
    subtipo: str
    etapa: str
    tempo_minimo: timedelta
    

@dataclass
class TipoEtapaData:
    nome: str
    buffer: int
    vagas: int
    grupo: Literal['pericia', 'objeto']


class Planilha:
    def __init__(self) -> None:
        xls = pd.ExcelFile('dados.ods', engine="odf")

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

        self.df_etapas = pd.read_excel(xls, 'etapas')
        self.df_etapas.columns = self.df_etapas.columns.str.strip()

        self.df_exames = pd.read_excel(xls, 'exames')
        self.df_exames.columns = self.df_exames.columns.str.strip()

        
    def gerar_qtd_objetos(self) -> int:
        return random.choices(self.values_qtd_objetos, self.probabilites_qtd_objetos)[0]

    def gerar_tipo_objeto(self) -> str:
        return random.choices(self.values_tipo_objeto, self.probabilites_tipo_objeto)[0]

    def gerar_subtipo_objeto(self, tipo: str) -> str:
        return random.choices(self.values_subtipo[tipo], self.probabilidades_subtipo[tipo])[0]

    def extrair_etapa(self, row: pd.Series) -> EtapaData:
        return EtapaData(
            row['Objeto'],
            row['Subtipo'],
            row['Etapa'],
            timedelta(
                hours=row['Tempo mínimo'].hour,
                minutes=row['Tempo mínimo'].minute,
                seconds=row['Tempo mínimo'].second,
                microseconds=row['Tempo mínimo'].microsecond
            ),
        )

    def get_tipos_etapa(self) -> list[TipoEtapaData]:
        return [TipoEtapaData(nome=row['Etapa'], vagas=row['Vagas'], buffer=row['Buffer'], grupo=row['Grupo']) for _, row in self.df_etapas.iterrows()]


    def get_etapas(self, objeto: str, subtipo: str) -> list[EtapaData]:
        df = self.df_exames[(self.df_exames['Objeto'] == objeto) & (self.df_exames['Subtipo'] == subtipo)]
        return [self.extrair_etapa(row) for _, row in df.iterrows()]
