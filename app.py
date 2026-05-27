import streamlit as st
import sqlite3
import pandas as pd
import os

from datetime import datetime

# ==================================
# CONFIGURACION PAGINA
# ==================================

st.set_page_config(
    page_title='🏆 Polla Mundialista HLC 2026',
    page_icon='⚽',
    layout='wide'
)

# ==================================
# CARGAR CSS
# ==================================

css_path = os.path.join(
    os.path.dirname(__file__),
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

# ==================================
# HERO PRINCIPAL
# ==================================

st.markdown(
    """
    <div style='
        background: linear-gradient(
            135deg,
            #06121f,
            #102844
        );
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        border: 2px solid gold;
        margin-bottom: 30px;
    '>

    <h1 style='
        color: gold;
        font-size: 70px;
        margin-bottom: 10px;
    '>
    🏆 POLLA MUNDIALISTA 2026
    </h1>

    <h3 style='
        color: white;
        font-size: 28px;
    '>
    ⚽ Hacienda La Cabaña 🌴
    </h3>

    </div>
    """,
    unsafe_allow_html=True
)

# ==================================
# CONTEO REGRESIVO
# ==================================

st.markdown('---')

st.markdown(
    """
    <h1 style='text-align:center;'>
    ⏳ Cuenta regresiva Mundial 2026
    </h1>
    """,
    unsafe_allow_html=True
)

fecha_mundial = datetime(
    2026,
    6,
    11,
    0,
    0
)

ahora = datetime.now()

diferencia = fecha_mundial - ahora

dias = diferencia.days
horas = diferencia.seconds // 3600
minutos = (diferencia.seconds % 3600) // 60

if diferencia.total_seconds() > 0:

    st.markdown(
        f"""
        <div style='
            background:#102844;
            padding:35px;
            border-radius:25px;
            text-align:center;
            border:2px solid gold;
        '>

        <h1 style='font-size:70px;color:gold;'>
        🏆 {dias} días
        </h1>

        <h2 style='color:white;'>
        ⏰ {horas} horas y {minutos} minutos
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.success(
        '🔥 EL MUNDIAL YA COMENZÓ 🔥'
    )

# ==================================
# AVANCE DEL MUNDIAL
# ==================================

st.markdown('---')

st.markdown(
    """
    <h1 style='text-align:center;'>
    🌍 Avance del Mundial
    </h1>
    """,
    unsafe_allow_html=True
)

# TOTAL PARTIDOS

total_partidos = pd.read_sql(
    '''
    SELECT COUNT(*) as total
    FROM partidos
    ''',
    conn
).iloc[0]['total']

# PARTIDOS JUGADOS

jugados = pd.read_sql(
    '''
    SELECT COUNT(*) as total
    FROM resultados
    ''',
    conn
).iloc[0]['total']

# RESTANTES

restantes = total_partidos - jugados

# PORCENTAJE

if total_partidos > 0:

    porcentaje = jugados / total_partidos

else:

    porcentaje = 0

# ==================================
# METRICAS
# ==================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        '⚽ Jugados',
        jugados
    )

with col2:

    st.metric(
        '🕒 Restantes',
        restantes
    )

with col3:

    st.metric(
        '🏆 Total',
        total_partidos
    )

st.progress(porcentaje)

st.write(
    f'🔥 {round(porcentaje * 100, 1)}% del Mundial completado'
)


# ==================================
# REGLAS
# ==================================

st.markdown('---')

st.markdown(
    """
    <h1 style='text-align:center;'>
    📜 REGLAS OFICIALES
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
### 💰 1. Inversión
La inversión por participante es de **$50.000 COP**, lo que permitirá participar durante TODO el Mundial.

---

### 📅 2. Fecha límite de pago
El plazo máximo para pagar la cuota es:

## 🗓️ 10/06/2026

(un día antes de iniciar el Mundial)

---

### ⚽ 3. Predicciones por fases

- Las predicciones de la fase de grupos deben quedar listas antes del primer partido del Mundial.
- NO podrán modificarse después de ser guardadas.
- Las siguientes fases se habilitarán conforme avancen las llaves:
  - Octavos
  - Cuartos
  - Semifinal
  - Tercer puesto
  - Final

---

### 🏆 4. Sistema de puntos

✅ **Ganador o empate correcto:** +1 punto

✅ **Marcador exacto:** +2 puntos

🔥 **BONUS marcador único:** +2 puntos extra si eres el único participante con el marcador exacto.

# 🚀 Máximo posible por partido: 5 puntos

---

### 🥇 5. Premio extra — Goleador del Mundial

Antes de iniciar el Mundial cada participante deberá elegir el jugador que crea será el goleador del torneo.

✅ Si acierta, ganará el premio extra.

⚠️ Se puede repetir jugador entre participantes.

En caso de empate:

1. Ganará quien tenga más puntos en la tabla general.
2. Si persiste el empate, el premio se repartirá.

---

### 🎖️ 6. Ganadores

🏆 1er Puesto

🥈 2do Puesto

🥉 3er Puesto

⚽ Premio Goleador del Mundial
"""
)



# ==================================
# FOOTER
# ==================================

st.markdown('---')

st.markdown(
    """
    <div style='
        text-align:center;
        padding:20px;
        color:gray;
    '>

    
    ⚽ Responsables: Carolina y Marco 🌴

    <br>

    Creado por Carito Barrios 

    </div>
    """,
    unsafe_allow_html=True
)