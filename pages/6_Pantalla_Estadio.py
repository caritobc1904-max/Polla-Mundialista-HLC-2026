import streamlit as st
import sqlite3
import pandas as pd
import os

css_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'assets',
    'style.css'
)

with open(css_path) as f:

    st.markdown(
        f'<style>{f.read()}</style>',
        unsafe_allow_html=True
    )
# =========================
# CONEXIÓN
# =========================

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

st.title("🏆 QUIÉN ACERTÓ CADA PARTIDO")

# =========================
# TRAER PARTIDOS CON RESULTADO
# =========================

partidos = pd.read_sql(
    """
    SELECT 
        p.id,
        p.equipo_a,
        p.equipo_b,
        r.goles_a,
        r.goles_b
    FROM partidos p
    INNER JOIN resultados r
        ON p.id = r.partido_id
    ORDER BY r.id DESC
    """,
    conn
)

if partidos.empty:
    st.warning("No hay resultados aún")
    st.stop()

# =========================
# SELECCIONAR PARTIDO
# =========================

opciones = partidos.apply(
    lambda x: f"{x['equipo_a']} vs {x['equipo_b']} ({x['goles_a']}-{x['goles_b']})",
    axis=1
)

partido_sel = st.selectbox("Selecciona partido", opciones)

partido = partidos.iloc[opciones[opciones == partido_sel].index[0]]

partido_id = partido["id"]

st.markdown("---")

st.subheader(f"📊 Resultados del partido")

st.write(f"{partido['equipo_a']} {partido['goles_a']} - {partido['goles_b']} {partido['equipo_b']}")

# =========================
# TRAER PREDICCIONES
# =========================

predicciones = pd.read_sql(
    """
    SELECT usuario, pred_a, pred_b, puntos
    FROM predicciones
    WHERE partido_id = ?
    ORDER BY puntos DESC
    """,
    conn,
    params=(int(partido_id),)
)

# =========================
# MOSTRAR COMPACTO
# =========================

st.markdown("## 🧠 Predicciones")

for _, row in predicciones.iterrows():

    usuario = row["usuario"]
    pred_a = row["pred_a"]
    pred_b = row["pred_b"]
    puntos = row["puntos"]

    # ESTADO
    if puntos >= 3:
        estado = "🔥 MARCADOR EXACTO"
        color = "#facc15"
    elif puntos == 1:
        estado = "✅ ACIERTO"
        color = "#22c55e"
    else:
        estado = "❌ SIN ACIERTO"
        color = "#ef4444"

    # =========================
    # TARJETA COMPACTA
    # =========================

    st.markdown(
      f"""
      <div style="
        background:#111827;
        padding:8px 12px;
        border-radius:10px;
        margin-bottom:6px;
        border-left:4px solid {color};
     ">
        <span style="color:white; font-size:14px; font-weight:600;">
            👤 {usuario}
        </span>

        <span style="color:#9ca3af; font-size:13px; margin-left:10px;">
            {pred_a} - {pred_b}
        </span>

        <div style="color:white; font-size:13px; font-weight:bold;">
            ⭐ {puntos}
        </div>

        <div style="color:{color}; font-size:11px;">
            {estado}
        </div>

     </div>
      """,
      unsafe_allow_html=True
    )

st.markdown('---')
