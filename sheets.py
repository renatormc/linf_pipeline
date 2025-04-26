from dataclasses import dataclass
from datetime import timedelta
import pandas as pd
import random
import openpyxl

# openpyxl.reader.excel.warnings.simplefilter(action='ignore')


@dataclass
class EtapaData:
    objeto: str
    subtipo: str
    etapa: str
    tempo_minimo: timedelta
    

@dataclass
class EquipamentoData:
    nome: str
    buffer: int
    quantidade: int
   
@dataclass
class PeritoData:
    nome: str
    sequencia: int

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

        self.df_equipamentos = pd.read_excel(xls, 'equipamentos')
        self.df_equipamentos.columns = self.df_equipamentos.columns.str.strip()

        self.df_exames = pd.read_excel(xls, 'exames')
        self.df_exames.columns = self.df_exames.columns.str.strip()

        self.df_peritos = pd.read_excel(xls, 'peritos')
        self.df_peritos.columns = self.df_peritos.columns.str.strip()

        
    def gerar_qtd_objetos(self) -> int:
        return random.choices(self.values_qtd_objetos, self.probabilites_qtd_objetos)[0]

    def gerar_tipo_objeto(self) -> str:
        return random.choices(self.values_tipo_objeto, self.probabilites_tipo_objeto)[0]

    def gerar_subtipo_objeto(self, tipo: str) -> str:
        return random.choices(self.values_subtipo[tipo], self.probabilidades_subtipo[tipo])[0]

    def extrair_etapa(self, row: pd.Series) -> EtapaData:
        try:
            x = row['Tempo mínimo']
            tempo_minimo = timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
        except:
            tempo_minimo = pd.to_timedelta(row['Tempo mínimo'])
        
        return EtapaData(
            row['Objeto'],
            row['Subtipo'],
            row['Etapa'],
            tempo_minimo
        )

    def get_equipamentos(self) -> list[EquipamentoData]:
        return [EquipamentoData(nome=row['Nome'], quantidade=row['Quantidade'], buffer=row['Buffer']) for _, row in self.df_equipamentos.iterrows()]

    def get_peritos(self) -> list[PeritoData]:
        return [PeritoData(nome=row["Nome"], sequencia=row['Sequência']) for _, row in self.df_peritos.iterrows()]


    def get_etapas(self, objeto: str, subtipo: str) -> list[EtapaData]:
        df = self.df_exames[(self.df_exames['Objeto'] == objeto) & (self.df_exames['Subtipo'] == subtipo)]
        return [self.extrair_etapa(row) for _, row in df.iterrows()]
