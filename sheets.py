from dataclasses import dataclass
from datetime import timedelta
import pandas as pd
import random
import openpyxl

# openpyxl.reader.excel.warnings.simplefilter(action='ignore')


@dataclass
class EtapaData:
    evidencia: str
    subtipo: str
    etapa: str
    tempo_minimo: timedelta
    

@dataclass
class EquipamentoData:
    nome: str
    buffer: int
    quantidade: int
   


class Planilha:
    def __init__(self) -> None:
        xls = pd.ExcelFile('dados.xlsx')

        df_stat_qtd_evidencias = pd.read_excel(xls, 'estatistica_qtd_evidencias')
        df_stat_qtd_evidencias.columns = df_stat_qtd_evidencias.columns.str.strip()
        self.values_qtd_evidencias = list(df_stat_qtd_evidencias['Qtd evidências'])
        total = df_stat_qtd_evidencias['Quantidade'].sum()
        self.probabilites_qtd_evidencias = list(map(lambda x: x/total, list(df_stat_qtd_evidencias['Quantidade'])))

        df_stat_tipo_evidencia = pd.read_excel(xls, 'estatistica_tipo')
        df_stat_tipo_evidencia.columns = df_stat_tipo_evidencia.columns.str.strip()
        self.values_tipo_evidencia = list(df_stat_tipo_evidencia['Tipo'])
        total = df_stat_tipo_evidencia['Quantidade'].sum()
        self.probabilites_tipo_evidencia = list(map(lambda x: x/total, list(df_stat_tipo_evidencia['Quantidade'])))

        df = pd.read_excel(xls, 'estatistica_subtipo')
        df.columns = df.columns.str.strip()

        self.values_subtipo: dict[str, list[str]] = {}
        self.probabilidades_subtipo: dict[str, list[float]] = {}
        for _, row in df_stat_tipo_evidencia.iterrows():
            tipo = row['Tipo']
            df2 = df[df['Evidência'] == tipo]
            self.values_subtipo[tipo] = list(df2['Subtipo'])
            total = df2['Quantidade'].sum()
            self.probabilidades_subtipo[tipo] = list(map(lambda x: x/total, list(df2['Quantidade'])))

        self.df_equipamentos = pd.read_excel(xls, 'equipamentos')
        self.df_equipamentos.columns = self.df_equipamentos.columns.str.strip()

        self.df_exames = pd.read_excel(xls, 'exames')
        self.df_exames.columns = self.df_exames.columns.str.strip()

        
    def gerar_qtd_evidencias(self) -> int:
        return random.choices(self.values_qtd_evidencias, self.probabilites_qtd_evidencias)[0]

    def gerar_tipo_evidencia(self) -> str:
        return random.choices(self.values_tipo_evidencia, self.probabilites_tipo_evidencia)[0]

    def gerar_subtipo_evidencia(self, tipo: str) -> str:
        return random.choices(self.values_subtipo[tipo], self.probabilidades_subtipo[tipo])[0]

    def extrair_etapa(self, row: pd.Series) -> EtapaData:
        try:
            x = row['Tempo mínimo']
            tempo_minimo = timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
        except:
            tempo_minimo = pd.to_timedelta(row['Tempo mínimo'])
        
        return EtapaData(
            row['Evidência'],
            row['Subtipo'],
            row['Etapa'],
            tempo_minimo
        )

    def get_equipamentos(self) -> list[EquipamentoData]:
        return [EquipamentoData(nome=row['Nome'], quantidade=row['Quantidade'], buffer=row['Buffer']) for _, row in self.df_equipamentos.iterrows()]


    def get_etapas(self, evidencia: str, subtipo: str) -> list[EtapaData]:
        df = self.df_exames[(self.df_exames['Evidência'] == evidencia) & (self.df_exames['Subtipo'] == subtipo)]
        return [self.extrair_etapa(row) for _, row in df.iterrows()]
