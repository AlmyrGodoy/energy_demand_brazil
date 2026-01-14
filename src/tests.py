"""
tests.py
---------
Módulo responsável pelos testes estatísticos formais
utilizados no projeto de demanda de energia.

Contém:
- Teste ADF
- Teste KPSS
- Funções agregadoras para análise de estacionariedade

Este módulo NÃO faz:
- Gráficos
- Prints
- Decisão visual
- Salvamento de arquivos

Ele apenas CALCULA e RETORNA resultados estruturados.
"""

from typing import Dict, List
import pandas as pd

from statsmodels.tsa.stattools import adfuller, kpss


# ============================================================
# Testes individuais
# ============================================================

def adf_test(
    series: pd.Series,
    maxlag: int | None = None,
    regression: str = "c"
) -> Dict:
    """
    Executa o teste ADF (Augmented Dickey-Fuller).

    H0: A série possui raiz unitária (não estacionária)

    Parameters
    ----------
    series : pd.Series
        Série temporal a ser testada
    maxlag : int ou None
        Número máximo de defasagens
    regression : str
        Tipo de regressão ("c", "ct", "ctt", "n")

    Returns
    -------
    dict
        Estatística, p-valor, lags e número de observações
    """

    stat, pvalue, lags, nobs, _, _ = adfuller(
        series.dropna(),
        maxlag=maxlag,
        regression=regression,
        autolag="AIC"
    )

    return {
        "teste": "ADF",
        "estatistica": stat,
        "p_valor": pvalue,
        "lags": lags,
        "n_obs": nobs
    }


def kpss_test(
    series: pd.Series,
    regression: str = "c",
    nlags: str = "auto"
) -> Dict:
    """
    Executa o teste KPSS.

    H0: A série é estacionária

    Parameters
    ----------
    series : pd.Series
        Série temporal a ser testada
    regression : str
        Tipo de regressão ("c" ou "ct")
    nlags : str
        Número de defasagens ("auto" recomendado)

    Returns
    -------
    dict
        Estatística, p-valor e número de lags
    """

    stat, pvalue, lags, _ = kpss(
        series.dropna(),
        regression=regression,
        nlags=nlags
    )

    return {
        "teste": "KPSS",
        "estatistica": stat,
        "p_valor": pvalue,
        "lags": lags
    }


# ============================================================
# Funções agregadoras
# ============================================================

def run_stationarity_tests(
    series: pd.Series,
    variable_name: str
) -> List[Dict]:
    """
    Executa ADF e KPSS para uma única série.

    Parameters
    ----------
    series : pd.Series
        Série temporal
    variable_name : str
        Nome da variável

    Returns
    -------
    list of dict
        Resultados dos testes
    """

    results = []

    adf_result = adf_test(series)
    adf_result["variavel"] = variable_name
    results.append(adf_result)

    kpss_result = kpss_test(series)
    kpss_result["variavel"] = variable_name
    results.append(kpss_result)

    return results


def build_stationarity_table(
    df: pd.DataFrame,
    variables: List[str]
) -> pd.DataFrame:
    """
    Constrói tabela consolidada de estacionariedade
    para múltiplas variáveis.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo as séries
    variables : list of str
        Lista de variáveis a serem testadas

    Returns
    -------
    pd.DataFrame
        Tabela com MultiIndex (variável, teste)
    """

    all_results = []

    for var in variables:
        results = run_stationarity_tests(df[var], var)
        all_results.extend(results)

    table = pd.DataFrame(all_results)

    table = table.set_index(["variavel", "teste"])
    table = table.sort_index()

    return table


# ============================================================
# Função auxiliar de decisão (opcional)
# ============================================================

def decision_stationarity(
    row: pd.Series,
    alpha: float = 0.05
) -> str:
    """
    Avalia a hipótese nula de cada teste com base no p-valor.

    Parameters
    ----------
    row : pd.Series
        Linha da tabela de resultados
    alpha : float
        Nível de significância

    Returns
    -------
    str
        Interpretação da hipótese nula
    """

    if row.name[1] == "ADF":
        return "Estacionária" if row["p_valor"] < alpha else "Não estacionária"

    if row.name[1] == "KPSS":
        return "Estacionária" if row["p_valor"] > alpha else "Não estacionária"

    return ""