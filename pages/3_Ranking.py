import streamlit as st
import pandas as pd
from logic import calcular_puntos
from logic import tabla_general

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