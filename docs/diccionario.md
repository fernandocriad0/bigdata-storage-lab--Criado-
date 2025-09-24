# Diccionario de Datos

| Campo | Descripción | Tipo | Reglas |
|-------|-------------|------|--------|
# Diccionario de Datos — Esquema Canónico

Este documento define el **esquema canónico** al cual deben transformarse todos los CSVs heterogéneos antes de ser almacenados en la capa **Silver**.

## Esquema Canónico

| Campo   | Descripción                       | Tipo de dato  | Formato / Unidad |
|---------|-----------------------------------|---------------|------------------|
| date    | Fecha de la transacción           | `date`        | `YYYY-MM-DD`     |
| partner | Nombre del socio / contraparte    | `string`      | Texto libre      |
| amount  | Monto de la operación             | `float`       | Euros (EUR)      |

---

## Mapeos Origen → Canónico

Ejemplos típicos de cómo mapear distintos esquemas de origen al canónico:

| Origen (campo) | Canónico (campo) | Transformación / Nota                  |
|----------------|------------------|----------------------------------------|
| fecha          | date             | Convertir formato `DD/MM/YYYY` → `YYYY-MM-DD` |
| transaction_dt | date             | Extraer substring de timestamp         |
| cliente        | partner          | Mapear directamente                    |
| counterparty   | partner          | Mapear directamente                    |
| importe        | amount           | Reemplazar comas → puntos, convertir a float |
| value_eur      | amount           | Asegurar cast a float                  |

> ⚠️ Nota: cualquier campo adicional en origen debe documentarse y, si no aplica, descartarse explícitamente.
