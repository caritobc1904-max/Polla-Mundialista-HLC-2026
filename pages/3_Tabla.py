import streamlit as st
from logic import tabla_general

st.title('🏆 Tabla General')

ranking = tabla_general()

st.dataframe(ranking, use_container_width=True)