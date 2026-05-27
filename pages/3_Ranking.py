import streamlit as st
import pandas as pd
import sqlite3
from logic import calcular_puntos
from logic import tabla_general
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

# ==================================
# CALCULAR PUNTOS
# ==================================

calcular_puntos()

# ==================================
# TITULO
# ==================================

st.title('🏆 Ranking Mundialista')

st.markdown('---')

# ==================================
# TABLA
# ==================================

tabla = tabla_general()

# POSICIONES
tabla.index = tabla.index + 1

tabla.index.name = 'Posición'

tabla.columns = [
    'Usuario',
    'Puntos'
]

# ==================================
# MOSTRAR TABLA
# ==================================

st.dataframe(
    tabla,
    use_container_width=True
)

st.markdown('---')

# ==================================
# TOP 3
# ==================================

st.subheader('🥇 Top 3')

top3 = tabla.head(3)

for i, row in top3.iterrows():

    st.write(
        f"{i}. "
        f"{row['Usuario']} "
        f"- {row['Puntos']} pts"
    )