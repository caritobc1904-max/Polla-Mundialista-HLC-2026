import streamlit as st
import sqlite3
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
conn = sqlite3.connect('mundial.db', check_same_thread=False)
st.title('🏆 Tabla General')

ranking = tabla_general()

if ranking.empty:
    st.info("No hay datos aún")
    st.stop()

if not ranking.empty:

    ranking.index = ranking.index + 1
    ranking.index.name = "Posición"

    ranking.columns = [
        "Usuario",
        "Puntos"
    ]

st.dataframe(ranking, use_container_width=True)

st.markdown('---')

# ==================================
# TOP 3
# ==================================

st.subheader('🥇 Top 3')

top3 = ranking.head(3)

for i, row in top3.iterrows():
    st.write(f"{i}. {row['Usuario']} - {row['Puntos']} pts")