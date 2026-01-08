import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INTERIM_DATA_PATH = BASE_DIR / "data" / "interim"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)


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

    data = pd.read_csv(INTERIM_DATA_PATH / "base_consolidada_real.csv")
    data["date"] = pd.to_datetime(data["date"])

    # Logs
    data["ln_demanda"] = np.log(data["demanda_energia"])
    data["ln_tarifa"] = np.log(data["tarifa_energia_real"])
    data["ln_pib"] = np.log(data["pib_real"])
    data["ln_importacoes"] = np.log(data["importacoes_petroleo"])

    # Dummies
    data = create_event_dummies(data)

    final_columns = [
        "date",
        "ln_demanda",
        "ln_tarifa",
        "ln_pib",
        "ln_importacoes",
        "d_2001",
        "d_2006",
        "d_2008",
        "d_2020"
    ]

    data[final_columns].to_csv(
        PROCESSED_DATA_PATH / "base_analitica.csv",
        index=False
    )

    print("✅ Base analítica criada com sucesso!")
