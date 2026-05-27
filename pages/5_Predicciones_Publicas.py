import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('mundial.db', check_same_thread=False)

st.title("📊 Predicciones Públicas")

# ==================================
# CONSULTA SEGURA
# ==================================

query = '''
SELECT
    p.id,
    p.equipo_a,
    p.equipo_b,
    pr.usuario,
    pr.pred_a,
    pr.pred_b
FROM predicciones pr
JOIN partidos p
ON pr.partido_id = p.id
ORDER BY p.id ASC, pr.usuario ASC
'''

data = pd.read_sql(query, conn)

if data.empty:
    st.warning("No hay predicciones aún")
    st.stop()

# ==================================
# CREAR COLUMNAS VISUALES
# ==================================

data["Partido"] = (
    data["equipo_a"] + " vs " + data["equipo_b"]
)

data["Predicción"] = (
    data["pred_a"].astype(str)
    + " - "
    + data["pred_b"].astype(str)
)

# ==================================
# ORDEN SEGURO (SIN KEY ERROR)
# ==================================

data = data.sort_values(["id", "usuario"])

# ==================================
# MOSTRAR AGRUPADO
# ==================================

for partido_id, grupo in data.groupby("id"):

    st.markdown("---")

    st.subheader(
        f"⚽ {grupo.iloc[0]['Partido']}"
    )

    tabla = grupo[["usuario", "Predicción"]]
    tabla.columns = ["Usuario", "Predicción"]

    st.dataframe(tabla, use_container_width=True)
    