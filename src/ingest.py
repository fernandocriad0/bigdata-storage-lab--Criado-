# Módulo de ingesta
# Funciones para cargar archivos CSV en la capa raw
import pandas as pd
from pandas import DataFrame
from typing import List
from datetime import datetime, timezone


def tag_lineage(df: DataFrame, source_name: str) -> DataFrame:
    """
    Añade metadatos de linaje al DataFrame:
    - 'source_file': nombre del archivo origen.
    - 'ingested_at': timestamp UTC ISO 8601.
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[DataFrame]) -> DataFrame:
    """
    Concatena varios DataFrames en un esquema estándar:
    - Columnas esperadas: date, partner, amount, source_file, ingested_at.
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])

    bronze = pd.concat(frames, ignore_index=True)

    # Reordenar columnas al esquema esperado
    cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    bronze = bronze[[c for c in cols if c in bronze.columns]]

    return bronze
