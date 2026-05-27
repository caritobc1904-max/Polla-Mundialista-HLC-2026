import streamlit as st
import sqlite3
import pandas as pd

# CONEXION
conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# PASSWORD ADMIN
PASSWORD = "lacabana2026"

# LOGIN ADMIN
st.title('⚙️ Panel Administrador')

password = st.text_input(
    'Ingrese contraseña admin',
    type='password'
)

if password != PASSWORD:

    st.warning('Contraseña incorrecta')

    st.stop()

st.success('Acceso autorizado')

st.markdown('---')

# =========================
# CREAR USUARIOS
# =========================

st.subheader('👥 Crear usuarios')

nuevo_usuario = st.text_input(
    'Nuevo usuario'
)

nuevo_password = st.text_input(
    'Contraseña usuario',
    type='password'
)

if st.button('Crear usuario'):

    try:

        cursor.execute(
            '''
            INSERT INTO usuarios(
                nombre,
                password
            )
            VALUES (?, ?)
            ''',
            (
                nuevo_usuario,
                nuevo_password
            )
        )

        conn.commit()

        st.success(
            'Usuario creado correctamente'
        )

    except:

        st.error(
            'Ese usuario ya existe'
        )

st.markdown('---')

# =========================
# VER USUARIOS
# =========================

st.subheader('📋 Usuarios registrados')

usuarios = pd.read_sql(
    'SELECT nombre FROM usuarios',
    conn
)

st.dataframe(
    usuarios,
    use_container_width=True
)

st.markdown('---')

# =========================
# CREAR PARTIDOS
# =========================

st.subheader('⚽ Crear partidos')

jornada = st.text_input(
    'Jornada'
)

fecha = st.text_input(
    'Fecha (2026-06-15)'
)

hora = st.text_input(
    'Hora (18:00)'
)

equipo_a = st.text_input(
    'Equipo A'
)

bandera_a = st.text_input(
    'Bandera A'
)

equipo_b = st.text_input(
    'Equipo B'
)

bandera_b = st.text_input(
    'Bandera B'
)

if st.button('Guardar partido'):

    cursor.execute(
        '''
        INSERT INTO partidos(
            jornada,
            fecha,
            hora,
            equipo_a,
            equipo_b,
            bandera_a,
            bandera_b
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            jornada,
            fecha,
            hora,
            equipo_a,
            equipo_b,
            bandera_a,
            bandera_b
        )
    )

    conn.commit()

    st.success(
        'Partido guardado correctamente'
    )

st.markdown('---')

# =========================
# VER PARTIDOS
# =========================

st.subheader('📅 Partidos registrados')

partidos = pd.read_sql(
    'SELECT * FROM partidos',
    conn
)

st.dataframe(
    partidos,
    use_container_width=True
)

st.markdown('---')

# =========================
# ACTUALIZAR RESULTADOS
# =========================

st.subheader('🏆 Actualizar resultados')

for _, partido in partidos.iterrows():

    st.markdown('---')

    st.subheader(
        f"{partido['bandera_a']} "
        f"{partido['equipo_a']} vs "
        f"{partido['bandera_b']} "
        f"{partido['equipo_b']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        gol_a = st.number_input(
            f"Goles {partido['equipo_a']}",
            min_value=0,
            key=f"a{partido['id']}"
        )

    with col2:

        gol_b = st.number_input(
            f"Goles {partido['equipo_b']}",
            min_value=0,
            key=f"b{partido['id']}"
        )

    if st.button(
        f"Actualizar resultado {partido['id']}"
    ):

        cursor.execute(
            '''
            UPDATE partidos
            SET gol_a=?,
                gol_b=?
            WHERE id=?
            ''',
            (
                gol_a,
                gol_b,
                partido['id']
            )
        )

        conn.commit()

        st.success(
            'Resultado actualizado'
        )

st.markdown('---')

# =========================
# VER PREDICCIONES
# =========================

st.subheader('📝 Predicciones registradas')

predicciones = pd.read_sql(
    '''
    SELECT
        usuario,
        partido_id,
        pred_a,
        pred_b
    FROM predicciones
    ''',
    conn
)

st.dataframe(
    predicciones,
    use_container_width=True
)

st.markdown('---')


# ==================================
# GOLEADORES REALES
# ==================================

st.subheader('⚽ Actualizar goleadores')

jugador = st.selectbox(
    'Jugador',
    [
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
        'Florian Wirtz'
    ]
)

goles = st.number_input(
    'Cantidad goles',
    min_value=0,
    step=1
)

if st.button(
    'Actualizar goleador'
):

    existente = cursor.execute(
        '''
        SELECT *
        FROM goleadores_real
        WHERE jugador=?
        ''',
        (jugador,)
    ).fetchone()

    if existente:

        cursor.execute(
            '''
            UPDATE goleadores_real
            SET goles=?
            WHERE jugador=?
            ''',
            (
                goles,
                jugador
            )
        )

    else:

        cursor.execute(
            '''
            INSERT INTO goleadores_real(
                jugador,
                goles
            )
            VALUES (?, ?)
            ''',
            (
                jugador,
                goles
            )
        )

    conn.commit()

    st.success(
        'Goleador actualizado'
    )

# ==================================
# TABLA GOLEADORES
# ==================================

tabla_goleadores = pd.read_sql(
    '''
    SELECT *
    FROM goleadores_real
    ORDER BY goles DESC
    ''',
    conn
)

st.dataframe(
    tabla_goleadores,
    use_container_width=True
)