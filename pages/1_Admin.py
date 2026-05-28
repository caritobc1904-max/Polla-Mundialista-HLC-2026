import streamlit as st
import sqlite3
import pandas as pd
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
# CONEXION
# ==================================

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# ==================================
# CREAR COLUMNA PAGO SI NO EXISTE
# ==================================

try:

    cursor.execute(
        '''
        ALTER TABLE usuarios
        ADD COLUMN pago INTEGER DEFAULT 0
        '''
    )

    conn.commit()

except:
    pass

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

# ==================================
# CONTROL PAGOS
# ==================================

st.markdown('---')

st.subheader('💰 Control de pagos')

usuarios_pago = pd.read_sql(
    '''
    SELECT nombre, pago
    FROM usuarios
    ''',
    conn
)

if not usuarios_pago.empty:

    usuario_pago = st.selectbox(
        'Selecciona usuario',
        usuarios_pago['nombre']
    )

    estado_actual = usuarios_pago[
        usuarios_pago['nombre'] == usuario_pago
    ]['pago'].values[0]

    texto_estado = (
        '✅ PAGADO'
        if estado_actual == 1
        else '❌ PENDIENTE'
    )

    st.info(
        f'Estado actual: {texto_estado}'
    )

    if st.button('Cambiar estado pago'):

        nuevo_estado = (
            0 if estado_actual == 1 else 1
        )

        cursor.execute(
            '''
            UPDATE usuarios
            SET pago=?
            WHERE nombre=?
            ''',
            (
                nuevo_estado,
                usuario_pago
            )
        )

        conn.commit()

        st.success(
            'Estado actualizado correctamente'
        )

        st.rerun()


# ==================================
# TABLA PAGOS
# ==================================

tabla_pagos = pd.read_sql(
    '''
    SELECT
        nombre,
        CASE
            WHEN pago = 1
            THEN '✅ PAGADO'
            ELSE '❌ PENDIENTE'
        END as estado
    FROM usuarios
    ''',
    conn
)

st.dataframe(
    tabla_pagos,
    use_container_width=True
)

# ==================================
# RESUMEN DINERO
# ==================================

st.markdown('---')

st.subheader('💵 Resumen financiero')

total_usuarios = pd.read_sql(
    '''
    SELECT COUNT(*) as total
    FROM usuarios
    ''',
    conn
).iloc[0]["total"]

usuarios_pagados = pd.read_sql(
    '''
    SELECT COUNT(*) as total
    FROM usuarios
    WHERE pago = 1
    ''',
    conn
).iloc[0]["total"]

usuarios_pendientes = (
    total_usuarios - usuarios_pagados
)

valor_inscripcion = 50000

recaudado = (
    usuarios_pagados * valor_inscripcion
)

faltante = (
    usuarios_pendientes * valor_inscripcion
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        '👥 Usuarios',
        total_usuarios
    )

with col2:

    st.metric(
        '✅ Pagados',
        usuarios_pagados
    )

with col3:

    st.metric(
        '💰 Recaudado',
        f'${recaudado:,.0f}'
    )

with col4:

    st.metric(
        '❌ Pendiente',
        f'${faltante:,.0f}'
    )

st.markdown('---')

# ==================================
# MOSTRAR PREDICCIONES PUBLICAS
# ==================================

st.markdown('---')

st.subheader('🌍 Predicciones públicas')

# CREAR TABLA CONFIG SI NO EXISTE
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS configuracion (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )
    '''
)

conn.commit()

# BUSCAR CONFIG
config = cursor.execute(
    '''
    SELECT valor
    FROM configuracion
    WHERE clave='mostrar_publicas'
    '''
).fetchone()

# SI NO EXISTE
if not config:

    cursor.execute(
        '''
        INSERT INTO configuracion(
            clave,
            valor
        )
        VALUES (?, ?)
        ''',
        (
            'mostrar_publicas',
            '0'
        )
    )

    conn.commit()

    mostrar = '0'

else:

    mostrar = config[0]

# ESTADO
if mostrar == '1':

    st.success(
        '✅ Predicciones públicas ACTIVADAS'
    )

else:

    st.error(
        '❌ Predicciones públicas OCULTAS'
    )

# BOTON CAMBIAR
if st.button('Cambiar estado predicciones públicas'):

    nuevo = '0'

    if mostrar == '0':

        nuevo = '1'

    cursor.execute(
        '''
        UPDATE configuracion
        SET valor=?
        WHERE clave='mostrar_publicas'
        ''',
        (nuevo,)
    )

    conn.commit()

    st.rerun()


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
        usuarios_lista['nombre'],
        key='select_eliminar_usuario'
    )

    if st.button(
        'Eliminar usuario',
        key='btn_eliminar_usuario'
    ):

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
        partidos['label'],
        key='select_eliminar_partido'
    )

    partido_id = int(
        partido_seleccionado.split(" - ")[0]
    )

    if st.button(
        '🗑️ Eliminar partido',
        key='btn_eliminar_partido'
    ):

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
    '🗑️ Borrar todos los goleadores',
    key='btn_borrar_goleadores'
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
    'Eliminar TODAS las predicciones',
    key='btn_eliminar_predicciones'
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
    'Eliminar TODOS los goleadores',
    key='btn_eliminar_todos_goleadores'
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
        historial["label"],
        key='select_eliminar_resultado'
    )

    registro_id = int(
        registro_sel.split(" - ")[0]
    )

    if st.button(
        "🗑️ Eliminar resultado",
        key='btn_eliminar_resultado'
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