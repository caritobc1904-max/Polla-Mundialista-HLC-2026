import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('mundial.db', check_same_thread=False)
cursor = conn.cursor()

st.title('📝 Predicciones')

nombre = st.text_input('Nombre del participante')

partidos = pd.read_sql('SELECT * FROM partidos', conn)

for _, partido in partidos.iterrows():

    st.subheader(f"{partido['equipo_a']} vs {partido['equipo_b']}")

    col1, col2 = st.columns(2)

    with col1:
        pred_a = st.number_input(
            partido['equipo_a'],
            min_value=0,
            key=f"preda{partido['id']}"
        )

    with col2:
        pred_b = st.number_input(
            partido['equipo_b'],
            min_value=0,
            key=f"predb{partido['id']}"
        )

    if st.button(f"Guardar Predicción {partido['id']}"):

        cursor.execute(
            '''
            INSERT INTO predicciones(
                participante,
                partido_id,
                pred_a,
                pred_b
            )
            VALUES (?, ?, ?, ?)
            ''',
            (nombre, partido['id'], pred_a, pred_b)
        )

        conn.commit()

        st.success('Predicción guardada')