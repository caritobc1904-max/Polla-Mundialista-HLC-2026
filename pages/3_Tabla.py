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

st.dataframe(ranking, use_container_width=True)