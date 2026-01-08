import pandas as pd
from pathlib import Path
from functools import reduce

# =========================
# Paths do projeto
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_INTERIM = BASE_DIR / "data" / "interim"
DATA_INTERIM.mkdir(parents=True, exist_ok=True)

# =========================
# Funções auxiliares
# =========================
def load_and_clean_series(file_path: Path, value_name: str):
    """
    Carrega série do CSV, padroniza nomes e converte data
    """
    df = pd.read_csv(file_path)
    df.columns = [c.lower().strip() for c in df.columns]

    df["date"] = (
        pd.to_datetime(df["raw date"], utc=True)
          .dt.tz_convert(None)
          .dt.normalize()
    )

    value_col = [c for c in df.columns if c.startswith("value")][0]
    df = df.rename(columns={value_col: value_name})

    return df[["date", value_name]].sort_values("date")


def convert_gwh_to_mwh(df, column):
    """
    Converte GWh para MWh
    """
    df = df.copy()
    df[column] = df[column] * 1000
    return df


def build_price_index(df, inflation_col, base=100):
    """
    Constrói índice de preços a partir de inflação mensal (% a.m.)
    """
    df = df.copy()

    # Converter % para taxa decimal
    df["inflation_rate"] = df[inflation_col] / 100

    # Índice acumulado
    df["price_index"] = (1 + df["inflation_rate"]).cumprod()

    # Normalizar para base escolhida (último período = 100)
    df["price_index"] = df["price_index"] / df["price_index"].iloc[-1] * base

    return df


def deflate(df, cols, index_col):
    """
    Deflaciona variáveis monetárias usando índice de preços
    """
    df = df.copy()
    base_index = df[index_col].iloc[-1]

    for col in cols:
        df[f"{col}_real"] = (df[col] / df[index_col]) * base_index

    return df

# =========================
# Pipeline principal
# =========================
if __name__ == "__main__":

    # ---------
    # Load
    # ---------
    demanda = load_and_clean_series(
        DATA_RAW / "demanda_energia_industrial.csv",
        "demanda_energia"
    )

    tarifa = load_and_clean_series(
        DATA_RAW / "tarifa_energia_industrial.csv",
        "tarifa_energia"
    )

    pib = load_and_clean_series(
        DATA_RAW / "pib.csv",
        "pib"
    )

    importacoes = load_and_clean_series(
        DATA_RAW / "importacoes_derivados_petroleo.csv",
        "importacoes_petroleo"
    )

    igpdi = load_and_clean_series(
        DATA_RAW / "igpdi.csv",
        "igpdi"
    )

    # ---------
    # Merge
    # ---------
    data = reduce(
        lambda l, r: pd.merge(l, r, on="date", how="inner"),
        [demanda, tarifa, pib, importacoes, igpdi]
    )

    # ---------
    # Transformações
    # ---------

    # Conversão de unidade da demanda
    data = convert_gwh_to_mwh(data, "demanda_energia")

    # Construção do índice de preços (IGP-DI)
    data = build_price_index(
        data,
        inflation_col="igpdi",
        base=100
    )

    # Deflação de variáveis monetárias
    data = deflate(
        data,
        cols=["tarifa_energia", "pib"],
        index_col="price_index"
    )

    # ---------
    # Limpeza final
    # ---------
    data = data.drop(
        columns=["igpdi", "inflation_rate", "price_index", "tarifa_energia", "pib"]
    )

    # ---------
    # Save
    # ---------
    data.to_csv(
        DATA_INTERIM / "base_consolidada_real.csv",
        index=False
    )

    print("✅ Base interim real criada com sucesso!")
