import pandas as pd
import statsmodels.api as sm
from typing import List


def fit_ols(
    df: pd.DataFrame,
    y: str,
    X: List[str],
    add_constant: bool = True
):
    """
    Estima um modelo de Regressão Linear por MQO (OLS).

    Parâmetros
    ----------
    df : pd.DataFrame
        Base de dados já tratada e com transformações aplicadas.
    y : str
        Nome da variável dependente.
    X : list[str]
        Lista com os nomes das variáveis explicativas.
    add_constant : bool, default=True
        Se True, adiciona intercepto ao modelo.

    Retorno
    -------
    results : statsmodels.regression.linear_model.RegressionResults
        Objeto do modelo estimado.
    """

    # Selecionar variáveis
    Y = df[y]
    X_mat = df[X]

    # Intercepto
    if add_constant:
        X_mat = sm.add_constant(X_mat)

    # Estimação MQO
    model = sm.OLS(Y, X_mat, missing="drop")
    results = model.fit()

    return results


def summarize_model(results):
    """
    Retorna o summary do modelo como texto.
    Útil para exportação ou logging.
    """
    return results.summary().as_text()


def extract_coefficients(results):
    """
    Extrai coeficientes, erros-padrão, estatísticas t e p-valores.

    Retorno
    -------
    pd.DataFrame
    """
    return pd.DataFrame({
        "coef": results.params,
        "std_err": results.bse,
        "t": results.tvalues,
        "p_value": results.pvalues
    })


def fitted_values(results) -> pd.Series:
    """
    Retorna os valores ajustados do modelo.
    """
    return results.fittedvalues


def residuals(results) -> pd.Series:
    """
    Retorna os resíduos do modelo.
    """
    return results.resid

def apply_robust_errors(results, cov_type: str = "HC1", maxlags: int | None = None):
    """
    Aplica erros-padrão robustos ao modelo estimado.

    Parâmetros
    ----------
    results : RegressionResults
        Modelo MQO estimado.
    cov_type : str
        Tipo de matriz robusta:
        - "HC0", "HC1", "HC2", "HC3" (White)
        - "HAC" (Newey-West)
    maxlags : int, opcional
        Número de defasagens para HAC.

    Retorno
    -------
    RegressionResults
        Modelo com erros-padrão robustos.
    """

    if cov_type == "HAC":
        if maxlags is None:
            raise ValueError("Para HAC é necessário informar maxlags.")
        return results.get_robustcov_results(
            cov_type="HAC",
            maxlags=maxlags
        )

    return results.get_robustcov_results(cov_type=cov_type)
