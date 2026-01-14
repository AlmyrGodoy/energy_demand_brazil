"""
utils.py
--------
Funções utilitárias do projeto.

Este módulo contém funções auxiliares que:
- Não fazem econometria
- Não tomam decisões estatísticas
- Não conhecem o modelo
- Apenas APOIAM o pipeline (IO, visualização, formatação)

Exemplo de uso:
- Salvar tabelas como imagem
- Padronizar saída gráfica
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def save_table_as_image(
    df: pd.DataFrame,
    filename: str,
    title: str,
    output_dir: Path | None = None,
    figsize: tuple = (14, 4),
    fontsize: int = 9,
    scale: tuple = (1, 1.5),
    dpi: int = 300
) -> None:
    """
    Salva um DataFrame como imagem (.png).

    Parameters
    ----------
    df : pd.DataFrame
        Tabela a ser salva
    filename : str
        Nome do arquivo (ex: 'stationarity_level.png')
    title : str
        Título do gráfico
    output_dir : Path ou None
        Diretório de saída. Se None, salva no diretório atual
    figsize : tuple
        Tamanho da figura
    fontsize : int
        Tamanho da fonte da tabela
    scale : tuple
        Escala da tabela
    dpi : int
        Resolução da imagem
    """

    if output_dir is None:
        output_dir = Path(".")

    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        rowLabels=df.index,
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(*scale)

    plt.title(title, pad=20)
    plt.savefig(
        output_dir / filename,
        dpi=dpi,
        bbox_inches="tight"
    )
    plt.close()
