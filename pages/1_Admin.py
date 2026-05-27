import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('mundial.db', check_same_thread=False)
cursor = conn.cursor()

st.title('⚙️ Panel Administrador')

st.subheader('Crear partido')

fecha = st.text_input('Fecha')
equipo_a = st.text_input('Equipo A')
equipo_b = st.text_input('Equipo B')

if st.button('Guardar partido'):

    cursor.execute(
        '''
        INSERT INTO partidos(fecha, equipo_a, equipo_b)
        VALUES (?, ?, ?)
        ''',
        (fecha, equipo_a, equipo_b)
    )

    conn.commit()

    st.success('Partido guardado')

st.subheader('Actualizar resultados')

partidos = pd.read_sql('SELECT * FROM partidos', conn)

for _, partido in partidos.iterrows():

    st.write(f"{partido['equipo_a']} vs {partido['equipo_b']}")

    col1, col2 = st.columns(2)

    with col1:
        gol_a = st.number_input(
            f"Gol {partido['equipo_a']}",
            min_value=0,
            key=f"a{partido['id']}"
        )

    with col2:
        gol_b = st.number_input(
            f"Gol {partido['equipo_b']}",
            min_value=0,
            key=f"b{partido['id']}"
        )

    if st.button(f"Actualizar {partido['id']}"):

        cursor.execute(
            '''
            UPDATE partidos
            SET gol_a=?, gol_b=?
            WHERE id=?
            ''',
            (gol_a, gol_b, partido['id'])
        )

        conn.commit()

        st.success('Resultado actualizado')