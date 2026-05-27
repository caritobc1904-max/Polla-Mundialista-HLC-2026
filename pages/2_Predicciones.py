import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

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
# CONEXION BASE DE DATOS
# ==================================

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# ==================================
# TITULO
# ==================================

st.title('📝 Predicciones Mundialistas')

# ==================================
# LOGIN
# ==================================

usuario = st.text_input('Usuario')

password = st.text_input(
    'Contraseña',
    type='password'
)

# ==================================
# VALIDAR USUARIO
# ==================================

usuario_db = cursor.execute(
    '''
    SELECT *
    FROM usuarios
    WHERE nombre=?
    AND password=?
    ''',
    (usuario, password)
).fetchone()

# ==================================
# SI LOGIN ES CORRECTO
# ==================================

if usuario and password:

    if not usuario_db:

        st.error(
            'Usuario o contraseña incorrectos'
        )

        st.stop()

    st.success(f'Bienvenido {usuario}')

    # ==================================
    # VALIDAR PAGO
    # ==================================

    estado_pago = cursor.execute(
        '''
        SELECT pago
        FROM usuarios
        WHERE nombre=?
        ''',
        (usuario,)
    ).fetchone()

    # SI NO EXISTE
    if estado_pago is None:

        pago = 0

    else:

        pago = estado_pago[0]

    # ==================================
    # BLOQUEAR SI NO HA PAGADO
    # ==================================

    if pago == 0:

        st.error(
            '❌ Aún no has realizado el pago.'
        )

        st.warning(
            'Debes pagar para habilitar las predicciones.'
        )

        st.stop()

    # ==================================
    # SI YA PAGÓ
    # ==================================

    st.success(
        '✅ Pago verificado correctamente'
    )

    st.markdown('---')

    # ==============================
    # OBTENER PARTIDOS
    # ==============================

    partidos = pd.read_sql(
        '''
        SELECT *
        FROM partidos
        ORDER BY fecha, hora
        ''',
        conn
    )

    # ==============================
    # SI NO HAY PARTIDOS
    # ==============================

    if partidos.empty:

        st.warning(
            'No hay partidos registrados'
        )

        st.stop()

    # ==============================
    # RECORRER PARTIDOS
    # ==============================

    for _, partido in partidos.iterrows():

        st.markdown('---')

        # ==========================
        # TITULO PARTIDO
        # ==========================

        st.subheader(
            f"{partido['bandera_a']} "
            f"{partido['equipo_a']} vs "
            f"{partido['bandera_b']} "
            f"{partido['equipo_b']}"
        )

        st.write(
            f"📅 {partido['jornada']}"
        )

        st.write(
            f"🕒 {partido['fecha']} "
            f"{partido['hora']}"
        )

        # ==================================
        # BLOQUEOS POR FASE
        # ==================================

        ahora = datetime.now()

        jornada = partido["jornada"]

        # FASE DE GRUPOS
        if jornada == "Grupos":

            fecha_cierre = datetime.strptime(
                "2026-06-11 00:00",
                "%Y-%m-%d %H:%M"
            )

        # OCTAVOS
        elif jornada == "Octavos":

            fecha_cierre = datetime.strptime(
                "2026-06-28 00:00",
                "%Y-%m-%d %H:%M"
            )

        # CUARTOS
        elif jornada == "Cuartos":

            fecha_cierre = datetime.strptime(
                "2026-07-04 00:00",
                "%Y-%m-%d %H:%M"
            )

        # SEMIFINAL
        elif jornada == "Semifinal":

            fecha_cierre = datetime.strptime(
                "2026-07-09 00:00",
                "%Y-%m-%d %H:%M"
            )

        # FINAL
        elif jornada == "Final":

            fecha_cierre = datetime.strptime(
                "2026-07-18 00:00",
                "%Y-%m-%d %H:%M"
            )

        else:

            fecha_cierre = datetime.now()

        # ==================================
        # BLOQUEADO
        # ==================================

        bloqueado = ahora >= fecha_cierre

        # ==========================
        # VALIDAR SI YA PREDIJO
        # ==========================

        existente = cursor.execute(
            '''
            SELECT *
            FROM predicciones
            WHERE usuario=?
            AND partido_id=?
            ''',
            (
                usuario,
                partido['id']
            )
        ).fetchone()

        # ==========================
        # SI YA PREDIJO
        # ==========================

        if existente:

            st.success(
                f"Tu predicción: "
                f"{existente[3]} - {existente[4]}"
            )

            st.info(
                'La predicción es definitiva '
                'y no puede modificarse'
            )

            continue

        # ==========================
        # SI PREDICCIONES CERRADAS
        # ==========================

        if bloqueado:

            st.error(
                '⛔ Predicciones cerradas '
                'para esta fase'
            )

            continue

        # ==========================
        # FORMULARIO
        # ==========================

        col1, col2 = st.columns(2)

        with col1:

            pred_a = st.number_input(
                partido['equipo_a'],
                min_value=0,
                step=1,
                key=f"a{partido['id']}"
            )

        with col2:

            pred_b = st.number_input(
                partido['equipo_b'],
                min_value=0,
                step=1,
                key=f"b{partido['id']}"
            )

        # ==========================
        # BOTON GUARDAR
        # ==========================

        if st.button(
            f"Guardar predicción "
            f"{partido['id']}"
        ):

            cursor.execute(
                '''
                INSERT INTO predicciones(
                    usuario,
                    partido_id,
                    pred_a,
                    pred_b
                )
                VALUES (?, ?, ?, ?)
                ''',
                (
                    usuario,
                    partido['id'],
                    pred_a,
                    pred_b
                )
            )

            conn.commit()

            st.success(
                'Predicción guardada '
                'correctamente'
            )

            st.rerun()