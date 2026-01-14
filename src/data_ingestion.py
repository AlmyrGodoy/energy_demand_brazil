import sys
from pathlib import Path

PROJECT_ROOT = Path("..").resolve()
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
from ipeadatapy import timeseries

from src.config import PROJECT_ROOT

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)

#Definir função para fazer dowload dos dados e salvar como csv na pasta data/raw

def download_series(series_code: str, filename: str):
    """
    Download a time series from IPEA API and save it as CSV in data/raw.
    """
    df = timeseries(series_code)
    
    df.to_csv(DATA_RAW / filename, index=False)
    
    print(f"Saved {filename}")

#Codigos dos dados que serão extraídos da API do IPEA
SERIES = {
    "demanda_energia_industrial.csv": "ELETRO12_CEEIND12",
    "pib.csv": "BM12_PIB12",
    "tarifa_energia_industrial.csv": "ELETRO12_CEETIND12",
    "importacoes_derivados_petroleo.csv": "FUNCEX12_MPPETCOMB2N12",
    "igpdi.csv": "IGP12_IGPDIG12",
}

if __name__ == "__main__":
    for filename, code in SERIES.items():
        download_series(code, filename)
