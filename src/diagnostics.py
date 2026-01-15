import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as stats

from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import (
    het_breuschpagan,
    het_white,
    acorr_breusch_godfrey
)


def test_normality(residuals: pd.Series) -> dict:
    """
    Teste de normalidade dos resíduos (Jarque-Bera),
    compatível com diferentes versões do SciPy.
    """

    jb_result = stats.jarque_bera(residuals)

    # Compatibilidade entre versões do scipy
    if len(jb_result) == 2:
        jb_stat, jb_pvalue = jb_result
        skewness = residuals.skew()
        kurtosis = residuals.kurtosis()
    else:
        jb_stat, jb_pvalue, skewness, kurtosis = jb_result

    return {
        "test": "Jarque-Bera",
        "statistic": jb_stat,
        "p_value": jb_pvalue,
        "skewness": skewness,
        "kurtosis": kurtosis
    }

def test_autocorrelation_dw(residuals: pd.Series) -> dict:
    """
    Teste de autocorrelação via Durbin-Watson.
    """

    dw_stat = durbin_watson(residuals)

    return {
        "test": "Durbin-Watson",
        "statistic": dw_stat
    }

def test_autocorrelation_bg(results, nlags: int = 1) -> dict:
    """
    Teste de autocorrelação Breusch-Godfrey.

    Parâmetros
    ----------
    results : RegressionResults
        Objeto do modelo estimado.
    nlags : int
        Número de defasagens.
    """

    bg_test = acorr_breusch_godfrey(results, nlags=nlags)

    return {
        "test": "Breusch-Godfrey",
        "statistic": bg_test[0],
        "p_value": bg_test[1],
        "f_stat": bg_test[2],
        "f_p_value": bg_test[3],
        "lags": nlags
    }

def test_heteroskedasticity_bp(results) -> dict:
    """
    Teste de heterocedasticidade de Breusch-Pagan.
    """

    bp_test = het_breuschpagan(
        results.resid,
        results.model.exog
    )

    return {
        "test": "Breusch-Pagan",
        "lm_stat": bp_test[0],
        "lm_p_value": bp_test[1],
        "f_stat": bp_test[2],
        "f_p_value": bp_test[3]
    }

def test_heteroskedasticity_white(results) -> dict:
    """
    Teste de heterocedasticidade de White.
    """

    white_test = het_white(
        results.resid,
        results.model.exog
    )

    return {
        "test": "White",
        "lm_stat": white_test[0],
        "lm_p_value": white_test[1],
        "f_stat": white_test[2],
        "f_p_value": white_test[3]
    }

def calculate_vif(results) -> pd.DataFrame:
    """
    Calcula o Fator de Inflação da Variância (VIF)
    para as variáveis explicativas do modelo.

    Retorno
    -------
    pd.DataFrame
        Variável, VIF e interpretação.
    """

    X = pd.DataFrame(
        results.model.exog,
        columns=results.model.exog_names
    )

    # Remove intercepto, se existir
    if "const" in X.columns:
        X = X.drop(columns=["const"])

    vif_data = []

    for i, col in enumerate(X.columns):
        vif_value = variance_inflation_factor(X.values, i)

        if vif_value <= 5:
            interpretation = "Sem multicolinearidade"
        elif vif_value <= 10:
            interpretation = "Multicolinearidade moderada"
        else:
            interpretation = "Multicolinearidade severa"

        vif_data.append({
            "variavel": col,
            "vif": vif_value,
            "resultado": interpretation
        })

    return pd.DataFrame(vif_data)


def interpret_test(test_name: str, p_value: float | None) -> str:
    """
    Interpreta o resultado do teste econométrico com base no p-valor.
    """

    if p_value is None:
        return "Não aplicável"

    if test_name == "Jarque-Bera":
        return (
            "Dados com normalidade"
            if p_value >= 0.05
            else "Dados sem normalidade"
        )

    if test_name in ["Breusch-Pagan", "White"]:
        return (
            "Dados Homocedásticos"
            if p_value >= 0.05
            else "Dados Heterocedásticos"
        )

    if test_name == "Breusch-Godfrey":
        return (
            "Sem autocorrelação"
            if p_value >= 0.05
            else "Com autocorrelação"
        )

    return "Resultado indefinido"

def run_all_diagnostics(results, bg_lags: int = 1) -> pd.DataFrame:
    """
    Executa todos os diagnósticos econométricos do modelo
    e adiciona interpretação automática dos resultados.
    """

    diagnostics = []

    diagnostics.append(test_normality(results.resid))
    diagnostics.append(test_autocorrelation_dw(results.resid))
    diagnostics.append(test_autocorrelation_bg(results, nlags=bg_lags))
    diagnostics.append(test_heteroskedasticity_bp(results))
    diagnostics.append(test_heteroskedasticity_white(results))

    df_diag = pd.DataFrame(diagnostics)

    # Coluna de interpretação
    df_diag["resultado"] = df_diag.apply(
        lambda row: interpret_test(
            row["test"],
            row.get("p_value")
        ),
        axis=1
    )

    return df_diag
