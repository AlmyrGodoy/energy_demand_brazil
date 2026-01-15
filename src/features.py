import sys
from pathlib import Path

PROJECT_ROOT = Path("..").resolve()
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import numpy as np

from src.config import DATA_INTERIM, DATA_PROCESSED

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

def create_event_dummies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["d_2001"] = 0
    df["d_2006"] = 0
    df["d_2008"] = 0
    df["d_2020"] = 0

    df.loc[df["date"] == "2001-07-01", "d_2001"] = 1
    df.loc[df["date"] == "2006-01-01", "d_2006"] = 1
    df.loc[df["date"].isin(["2008-12-01", "2009-01-01"]), "d_2008"] = 1
    df.loc[df["date"] == "2020-04-01", "d_2020"] = 1

    return df


if __name__ == "__main__":

    # ---------
    # Load
    # ---------
    data = pd.read_csv(DATA_INTERIM / "base_consolidada_real.csv")
    data["date"] = pd.to_datetime(data["date"])

    # ---------
    # Dummies estruturais
    # ---------
    data = create_event_dummies(data)

    # ---------
    # Seleção final (dados em nível)
    # ---------
    final_columns = [
        "date",
        "demanda_energia",
        "tarifa_energia_real",
        "pib_real",
        "importacoes_petroleo",
        "d_2001",
        "d_2006",
        "d_2008",
        "d_2020"
    ]

    data[final_columns].to_csv(
        DATA_PROCESSED / "base_analitica.csv",
        index=False
    )

    print("✅ Base analítica criada com sucesso!")