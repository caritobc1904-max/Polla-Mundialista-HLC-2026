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
    
conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

st.title('⚽ Goleador del Mundial')

# ==================================
# LISTA JUGADORES
# ==================================

jugadores = [

    'Kylian Mbappé',
    'Vinicius Jr',
    'Erling Haaland',
    'Harry Kane',
    'Julián Álvarez',
    'Lautaro Martínez',
    'Raphinha',
    'Rodrygo',
    'Luis Díaz',
    'Cristiano Ronaldo',
    'Lionel Messi',
    'Lamine Yamal',
    'Pedri',
    'Bruno Fernandes',
    'Darwin Núñez',
    'Alexander Isak',
    'Bukayo Saka',
    'Jamal Musiala',
    'Florian Wirtz',
    'Otro'
]

# ==================================
# LOGIN
# ==================================

usuario = st.text_input('Usuario')

password = st.text_input(
    'Contraseña',
    type='password'
)

usuario_db = cursor.execute(
    '''
    SELECT *
    FROM usuarios
    WHERE nombre=?
    AND password=?
    ''',
    (usuario, password)
).fetchone()

if usuario and password:

    if not usuario_db:

        st.error(
            'Usuario o contraseña incorrectos'
        )

        st.stop()

    # ==============================
    # VALIDAR SI YA REGISTRO
    # ==============================

    existente = cursor.execute(
        '''
        SELECT *
        FROM goleador_mundial
        WHERE usuario=?
        ''',
        (usuario,)
    ).fetchone()

    # ==============================
    # SI YA REGISTRO
    # ==============================

    if existente:

        st.success(
            f"Goleador elegido: "
            f"{existente[2]}"
        )

        st.info(
            'La elección es definitiva '
            'y no puede modificarse'
        )

    else:

        st.subheader(
            'Selecciona el goleador'
        )

        goleador = st.selectbox(
            'Jugador',
            jugadores
        )

        # SI ES OTRO
        if goleador == 'Otro':

            goleador = st.text_input(
                'Escribe el jugador'
            )

        # BOTON
        if st.button(
            'Guardar goleador'
        ):

            cursor.execute(
                '''
                INSERT INTO goleador_mundial(
                    usuario,
                    goleador
                )
                VALUES (?, ?)
                ''',
                (
                    usuario,
                    goleador
                )
            )

            conn.commit()

            st.success(
                'Goleador registrado correctamente'
            )

            st.rerun()

st.markdown('---')

# ==================================
# TABLA USUARIOS GOLEADOR
# ==================================

st.subheader(
    '🏆 Ranking Goleador Mundial'
)

tabla_usuarios = pd.read_sql(
    '''
    SELECT
        gm.usuario,
        gm.goleador,
        COALESCE(gr.goles, 0) as goles
    FROM goleador_mundial gm

    LEFT JOIN goleadores_real gr
    ON gm.goleador = gr.jugador

    ORDER BY goles DESC
    ''',
    conn
)

if not tabla_usuarios.empty:

    # POSICIONES
    tabla_usuarios.index = (
        tabla_usuarios.index + 1
    )

    tabla_usuarios.index.name = 'Posición'

    tabla_usuarios.columns = [
        'Usuario',
        'Jugador elegido',
        'Goles'
    ]

    st.dataframe(
        tabla_usuarios,
        use_container_width=True
    )

    st.markdown('---')

    # TOP 3
    st.subheader('🥇 Top goleadores')

    top3 = tabla_usuarios.head(3)

    for i, row in top3.iterrows():

        st.write(
            f"{i}. "
            f"{row['Usuario']} "
            f"- {row['Jugador elegido']} "
            f"({row['Goles']} goles)"
        )