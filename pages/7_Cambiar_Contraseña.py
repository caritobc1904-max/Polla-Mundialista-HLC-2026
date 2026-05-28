import streamlit as st
import sqlite3
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
# TITULO
# ==================================

st.title('🔒 Cambiar contraseña')

# ==================================
# LOGIN
# ==================================

usuario = st.text_input('Usuario')

password_actual = st.text_input(
    'Contraseña actual',
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
    (
        usuario,
        password_actual
    )
).fetchone()

# ==================================
# NUEVA PASSWORD
# ==================================

if usuario and password_actual:

    if not usuario_db:

        st.error(
            'Usuario o contraseña incorrectos'
        )

        st.stop()

    st.success(
        '✅ Usuario verificado'
    )

    nueva_password = st.text_input(
        'Nueva contraseña',
        type='password'
    )

    repetir_password = st.text_input(
        'Repetir nueva contraseña',
        type='password'
    )

    # ==================================
    # CAMBIAR
    # ==================================

    if st.button('Guardar nueva contraseña'):

        if len(nueva_password) < 4:

            st.warning(
                'La contraseña debe tener mínimo 4 caracteres'
            )

            st.stop()

        if nueva_password != repetir_password:

            st.error(
                'Las contraseñas no coinciden'
            )

            st.stop()

        cursor.execute(
            '''
            UPDATE usuarios
            SET password=?
            WHERE nombre=?
            ''',
            (
                nueva_password,
                usuario
            )
        )

        conn.commit()

        st.success(
            '🔐 Contraseña actualizada correctamente'
        )
    