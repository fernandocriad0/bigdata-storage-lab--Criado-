# Módulo de validación
# Funciones para verificar calidad de datos (tipos, nulos, duplicados)
import pandas as pd
from pandas import DataFrame
from typing import List


def basic_checks(df: DataFrame) -> List[str]:
    """
    Realiza validaciones básicas sobre un DataFrame en esquema canónico.
    Devuelve una lista de errores encontrados.
    """
    errors: List[str] = []

    # 1. Columnas canónicas presentes
    required = {"date", "partner", "amount"}
    missing = required - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(missing)}")

    # 2. Verificar tipo datetime en date
    if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
        errors.append("La columna 'date' no es de tipo datetime")

    # 3. Verificar amount numérico y >= 0
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("La columna 'amount' no es numérica")
        elif (df["amount"] < 0).any():
            errors.append("Existen valores negativos en 'amount'")

    return errors
