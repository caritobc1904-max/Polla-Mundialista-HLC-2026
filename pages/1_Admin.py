import streamlit as st
import sqlite3
import pandas as pd

# ==================================
# CONEXION
# ==================================

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# ==================================
# PASSWORD ADMIN
# ==================================

PASSWORD = "lacabana2026"

# ==================================
# LOGIN ADMIN
# ==================================

st.title('⚙️ Panel Administrador')

password = st.text_input(
    'Ingrese contraseña admin',
    type='password'
)

if password != PASSWORD:

    st.warning('Contraseña incorrecta')
    st.stop()

st.success('Acceso autorizado')

# ==================================
# LIMPIAR IDS CORRUPTOS
# ==================================

try:

    resultados_fix = pd.read_sql(
        '''
        SELECT *
        FROM resultados
        ''',
        conn
    )

    for _, row in resultados_fix.iterrows():

        try:

            int(row["partido_id"])

        except:

            cursor.execute(
                '''
                DELETE FROM resultados
                WHERE id = ?
                ''',
                (row["id"],)
            )

    conn.commit()

except:
    pass

st.markdown('---')

# ==================================
# CREAR USUARIOS
# ==================================

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

# ==================================
# VER USUARIOS
# ==================================

st.subheader('📋 Usuarios registrados')

usuarios = pd.read_sql(
    '''
    SELECT nombre
    FROM usuarios
    ''',
    conn
)

st.dataframe(
    usuarios,
    use_container_width=True
)

st.markdown('---')

# ==================================
# CREAR PARTIDOS
# ==================================

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

# ==================================
# VER PARTIDOS
# ==================================

st.subheader('📅 Partidos registrados')

partidos = pd.read_sql(
    '''
    SELECT *
    FROM partidos
    ''',
    conn
)

st.dataframe(
    partidos,
    use_container_width=True
)

st.markdown('---')

# ==================================
# ACTUALIZAR RESULTADOS
# ==================================

st.subheader('⚽ Actualizar resultado oficial')

partidos = pd.read_sql(
    '''
    SELECT id, equipo_a, equipo_b
    FROM partidos
    ''',
    conn
)

if not partidos.empty:

    partidos["label"] = (
        partidos["equipo_a"]
        + " vs "
        + partidos["equipo_b"]
    )

    partido_sel = st.selectbox(
        "Selecciona partido",
        partidos["label"]
    )

    partido_id = partidos.loc[
        partidos["label"] == partido_sel,
        "id"
    ].values[0]

    goles_a = st.number_input(
        "Goles equipo A",
        min_value=0,
        step=1
    )

    goles_b = st.number_input(
        "Goles equipo B",
        min_value=0,
        step=1
    )

    if st.button("💾 Guardar resultado oficial"):

        fila = partidos[
            partidos["id"] == partido_id
        ].iloc[0]

        equipo_a = fila["equipo_a"]
        equipo_b = fila["equipo_b"]

        # ELIMINAR RESULTADO ANTERIOR
        cursor.execute(
            '''
            DELETE FROM resultados
            WHERE partido_id = ?
            ''',
            (int(partido_id),)
        )

        # INSERTAR RESULTADO NUEVO
        cursor.execute(
            '''
            INSERT INTO resultados (
                partido_id,
                equipo_a,
                equipo_b,
                goles_a,
                goles_b
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (
                int(partido_id),
                equipo_a,
                equipo_b,
                int(goles_a),
                int(goles_b)
            )
        )

        conn.commit()

        # RECALCULAR PUNTOS
        from logic import calcular_puntos

        calcular_puntos()

        st.success(
            "Resultado guardado correctamente ⚽"
        )

        st.rerun()

st.markdown('---')

# ==================================
# HISTORIAL RESULTADOS
# ==================================

st.subheader('📊 Historial de resultados')

historial = pd.read_sql(
    '''
    SELECT *
    FROM resultados
    ORDER BY id DESC
    ''',
    conn
)

st.dataframe(
    historial,
    use_container_width=True
)

st.markdown('---')

# ==================================
# VER PREDICCIONES
# ==================================

st.subheader('📝 Predicciones registradas')

predicciones = pd.read_sql(
    '''
    SELECT
        usuario,
        partido_id,
        pred_a,
        pred_b,
        puntos
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

st.markdown('---')

# ==================================
# ELIMINAR USUARIOS
# ==================================

st.subheader('🗑️ Eliminar usuarios')

usuarios_lista = pd.read_sql(
    '''
    SELECT nombre
    FROM usuarios
    ''',
    conn
)

if not usuarios_lista.empty:

    usuario_eliminar = st.selectbox(
        'Selecciona usuario',
        usuarios_lista['nombre']
    )

    if st.button('Eliminar usuario'):

        cursor.execute(
            '''
            DELETE FROM usuarios
            WHERE nombre=?
            ''',
            (usuario_eliminar,)
        )

        cursor.execute(
            '''
            DELETE FROM predicciones
            WHERE usuario=?
            ''',
            (usuario_eliminar,)
        )

        cursor.execute(
            '''
            DELETE FROM goleador_mundial
            WHERE usuario=?
            ''',
            (usuario_eliminar,)
        )

        conn.commit()

        st.success(
            'Usuario eliminado correctamente'
        )

        st.rerun()

st.markdown('---')

# ==================================
# ELIMINAR PARTIDOS
# ==================================

st.subheader('⚽ Eliminar partidos')

partidos = pd.read_sql(
    '''
    SELECT id, equipo_a, equipo_b
    FROM partidos
    ''',
    conn
)

if not partidos.empty:

    partidos['label'] = (
        partidos['id'].astype(str)
        + " - "
        + partidos['equipo_a']
        + " vs "
        + partidos['equipo_b']
    )

    partido_seleccionado = st.selectbox(
        'Selecciona el partido',
        partidos['label']
    )

    partido_id = int(
        partido_seleccionado.split(" - ")[0]
    )

    if st.button('🗑️ Eliminar partido'):

        cursor.execute(
            '''
            DELETE FROM predicciones
            WHERE partido_id=?
            ''',
            (partido_id,)
        )

        cursor.execute(
            '''
            DELETE FROM resultados
            WHERE partido_id=?
            ''',
            (partido_id,)
        )

        cursor.execute(
            '''
            DELETE FROM partidos
            WHERE id=?
            ''',
            (partido_id,)
        )

        conn.commit()

        st.success(
            'Partido eliminado correctamente ⚽'
        )

        st.rerun()

else:

    st.warning(
        'No hay partidos registrados'
    )

st.markdown('---')

# ==================================
# LIMPIAR GOLEADORES
# ==================================

st.subheader('🥇 Eliminar goleadores')

if st.button(
    '🗑️ Borrar todos los goleadores'
):

    cursor.execute(
        "DELETE FROM goleador_mundial"
    )

    cursor.execute(
        "DELETE FROM goleadores_real"
    )

    conn.commit()

    st.success(
        'Goleadores eliminados correctamente'
    )

    st.rerun()

st.markdown('---')

# ==================================
# REINICIAR SISTEMA
# ==================================

st.subheader('🚨 Reiniciar sistema')

if st.button(
    'Eliminar TODAS las predicciones'
):

    cursor.execute(
        '''
        DELETE FROM predicciones
        '''
    )

    conn.commit()

    st.success(
        'Predicciones eliminadas'
    )

if st.button(
    'Eliminar TODOS los goleadores'
):

    cursor.execute(
        '''
        DELETE FROM goleador_mundial
        '''
    )

    conn.commit()

    st.success(
        'Goleadores eliminados'
    )

st.markdown('---')

# ==================================
# ELIMINAR HISTORIAL
# ==================================

st.subheader('🗑️ Eliminar historial de resultados')

historial = pd.read_sql(
    '''
    SELECT
        id,
        equipo_a,
        equipo_b,
        goles_a,
        goles_b
    FROM resultados
    ORDER BY id DESC
    ''',
    conn
)

if not historial.empty:

    historial["label"] = (
        historial["id"].astype(str)
        + " - "
        + historial["equipo_a"]
        + " vs "
        + historial["equipo_b"]
        + " ("
        + historial["goles_a"].astype(str)
        + "-"
        + historial["goles_b"].astype(str)
        + ")"
    )

    registro_sel = st.selectbox(
        "Selecciona resultado",
        historial["label"]
    )

    registro_id = int(
        registro_sel.split(" - ")[0]
    )

    if st.button(
        "🗑️ Eliminar resultado"
    ):

        cursor.execute(
            '''
            DELETE FROM resultados
            WHERE id=?
            ''',
            (registro_id,)
        )

        conn.commit()

        st.success(
            "Resultado eliminado correctamente ⚽"
        )

        st.rerun()

else:

    st.info(
        "No hay historial de resultados"
    )
