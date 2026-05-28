import streamlit as st
import pandas as pd
import os

from logic import calcular_puntos, tabla_general

# ==================================
# CSS
# ==================================

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

# ==================================
# TITULO
# ==================================

st.title('🏆 Ranking Mundialista')
st.markdown('---')

# ==================================
# BOTÓN SEGURO (IMPORTANTE)
# ==================================

if st.button("🔄 Actualizar ranking"):
    calcular_puntos()
    st.success("Ranking actualizado")

# ==================================
# TABLA GENERAL
# ==================================

tabla = tabla_general()

if tabla.empty:
    st.info("No hay datos aún")
    st.stop()

# POSICIONES
tabla.index = tabla.index + 1
tabla.index.name = "Posición"

tabla.columns = ["Usuario", "Puntos"]

# ==================================
# MOSTRAR TABLA
# ==================================

st.dataframe(tabla, use_container_width=True)

st.markdown('---')

# ==================================
# TOP 3
# ==================================

st.subheader('🥇 Top 3')

top3 = tabla.head(3)

for i, row in top3.iterrows():
    st.write(f"{i}. {row['Usuario']} - {row['Puntos']} pts")