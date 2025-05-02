from models import *
import pandas as pd
import config
import matplotlib.pyplot as plt

df = pd.read_json(config.APPDIR / ".local/results.json")
df['tempo_espera_medio'] = df['tempo_espera'] / df['objetos_finalizados']
df.set_index("cenario", inplace=True)


def grafico_pericias_finalizadas():
    df['pericias_finalizadas'].plot.bar()
    plt.xlabel('Cenário')
    plt.ylabel('Perícias finalizadas')
    plt.tight_layout()  # Optional: adjusts layout to prevent cutoff
    plt.savefig(".local/pericias_finalizadas.png")  # Save the figure


def grafico_objetos_finalizados():
    df['objetos_finalizados'].plot.bar()
    plt.xlabel('Cenário')
    plt.ylabel('Objetos finalizados')
    plt.tight_layout()  # Optional: adjusts layout to prevent cutoff
    plt.savefig(".local/objetos_finalizados.png")  # Save the figure
    # plt.show()

def grafico_tempo_espera():
    df['tempo_espera_medio'].plot.bar()
    plt.xlabel('Cenário')
    plt.ylabel('Tempo de espera médio')
    plt.tight_layout()
    plt.savefig(".local/tempo_espera.png")
    # plt.show()

grafico_pericias_finalizadas()
grafico_objetos_finalizados()
grafico_tempo_espera()