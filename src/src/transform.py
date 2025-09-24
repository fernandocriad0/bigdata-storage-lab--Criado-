src/transform.py
import pandas as pd
from pandas import DataFrame
from typing import Dict


def normalize_columns(df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
    """
    Normaliza columnas de un DataFrame según el esquema canónico:
    - Renombra columnas usando mapping origen→canónico.
    - Convierte 'date' a datetime ISO.
    - Limpia 'partner' (espacios en extremos).
    - Normaliza 'amount' (quita símbolo €, cambia coma→punto, convierte a float).
    """
    # Renombrar columnas
    df = df.rename(columns=mapping)

    # Normalizar fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", infer_datetime_format=True)

    # Normalizar partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(".", "", regex=False)   # quita separador de miles con punto
            .str.replace(",", ".", regex=False)  # convierte coma decimal a punto
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df


def to_silver(bronze: DataFrame) -> DataFrame:
    """
    Agrega datos desde capa Bronze a Silver:
    - Agrupa por partner y mes.
    - Suma amount por grupo.
    - Columna 'month' es primer día del mes (Timestamp).
    """
    if not {"date", "partner", "amount"}.issubset(bronze.columns):
        raise ValueError("Bronze debe contener columnas canónicas: date, partner, amount")

    bronze = bronze.copy()
    bronze["month"] = bronze["date"].dt.to_period("M").dt.to_timestamp()

    silver = (
        bronze.groupby(["partner", "month"], as_index=False)
        .agg({"amount": "sum"})
    )

    return silver

