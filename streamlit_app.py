# Streamlit app para el laboratorio "De CSVs heterogéneos a un almacén analítico confiable"
# Punto de entrada de la aplicación
import io
import pandas as pd
import streamlit as st
from typing import List

# Importar funciones del pipeline
from src.ingest import tag_lineage, concat_bronze
from src.transform import normalize_columns, to_silver
from src.validate import basic_checks


# ------------------------
# Configuración de página
# ------------------------
st.set_page_config(
    page_title="Laboratorio Big Data - Almacén Analítico",
    layout="wide"
)

st.title("📊 De CSVs heterogéneos a un almacén analítico confiable")

st.markdown(
    """
    Esta aplicación permite subir múltiples archivos CSV, normalizarlos a un esquema
    canónico (`date`, `partner`, `amount`), validar calidad, y derivar un conjunto
    **Bronze** (crudo+linaje) y **Silver** (agregado por mes).
    """
)

# ------------------------
# Sidebar: configuración
# ------------------------
st.sidebar.header("Configuración de columnas origen")

date_col = st.sidebar.text_input("Columna fecha (origen)", "fecha")
partner_col = st.sidebar.text_input("Columna socio/partner (origen)", "cliente")
amount_col = st.sidebar.text_input("Columna monto (origen)", "importe")

mapping = {
    date_col: "date",
    partner_col: "partner",
    amount_col: "amount",
}

st.sidebar.markdown("---")
uploaded_files = st.sidebar.file_uploader(
    "Subir archivos CSV",
    type=["csv"],
    accept_multiple_files=True
)

# ------------------------
# Procesamiento
# ------------------------
bronze_frames: List[pd.DataFrame] = []

if uploaded_files:
    for uploaded in uploaded_files:
        try:
            df = pd.read_csv(uploaded, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded, encoding="latin-1")

        df = normalize_columns(df, mapping)
        df = tag_lineage(df, uploaded.name)
        bronze_frames.append(df)

    # Unificar capa Bronze
    bronze = concat_bronze(bronze_frames)

    st.subheader("📂 Capa Bronze (unificada)")
    st.dataframe(bronze.head(20))

    # Validaciones
    errors = basic_checks(bronze)
    if errors:
        st.error("❌ Se encontraron problemas de validación:")
        for e in errors:
            st.write(f"- {e}")
    else:
        st.success("✅ Validaciones básicas superadas")

        # Derivar capa Silver
        silver = to_silver(bronze)

        st.subheader("💾 Capa Silver (agregada por partner × mes)")
        st.dataframe(silver.head(20))

        # KPIs simples
        st.markdown("### Indicadores Clave (KPIs)")
        total_amount = silver["amount"].sum()
        top_partner = silver.sort_values("amount", ascending=False).iloc[0]

        col1, col2 = st.columns(2)
        col1.metric("Monto total (EUR)", f"{total_amount:,.2f}")
        col2.metric("Partner principal", f"{top_partner['partner']} ({top_partner['amount']:,.2f} EUR)")

        # Visualización
        st.markdown("### Evolución mensual (monto total)")
        monthly = silver.groupby("month", as_index=False)["amount"].sum()
        st.bar_chart(monthly.set_index("month"))

        # Descargas
        st.markdown("### Descargas")
        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        silver_csv = silver.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Descargar Bronze (CSV)",
            data=bronze_csv,
            file_name="bronze.csv",
            mime="text/csv"
        )

        st.download_button(
            label="⬇️ Descargar Silver (CSV)",
            data=silver_csv,
            file_name="silver.csv",
            mime="text/csv"
        )
else:
    st.info("Sube uno o más archivos CSV desde la barra lateral para comenzar.")
