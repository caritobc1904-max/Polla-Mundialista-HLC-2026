import sqlite3
import pandas as pd
import os

# =========================================
# RUTA BASE DE DATOS
# =========================================

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "mundial.db"
)

# =========================================
# CALCULAR PUNTOS
# =========================================

def calcular_puntos():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    cursor = conn.cursor()

    # =========================================
    # CREAR COLUMNA PUNTOS SI NO EXISTE
    # =========================================

    try:

        cursor.execute(
            '''
            ALTER TABLE predicciones
            ADD COLUMN puntos INTEGER DEFAULT 0
            '''
        )

        conn.commit()

    except:
        pass

    # =========================================
    # RESETEAR PUNTOS
    # =========================================

    cursor.execute(
        '''
        UPDATE predicciones
        SET puntos = 0
        '''
    )

    conn.commit()

    # =========================================
    # TRAER RESULTADOS OFICIALES
    # =========================================

    resultados = pd.read_sql(
        '''
        SELECT
            partido_id,
            goles_a,
            goles_b
        FROM resultados
        ''',
        conn
    )

    # =========================================
    # RECORRER RESULTADOS
    # =========================================

    for _, resultado in resultados.iterrows():

        # =========================================
        # VALIDAR IDS
        # =========================================

        partido_id = pd.to_numeric(
            resultado["partido_id"],
            errors="coerce"
        )

        if pd.isna(partido_id):
            continue

        partido_id = int(partido_id)

        # =========================================
        # VALIDAR GOLES
        # =========================================

        gol_a = pd.to_numeric(
            resultado["goles_a"],
            errors="coerce"
        )

        gol_b = pd.to_numeric(
            resultado["goles_b"],
            errors="coerce"
        )

        if pd.isna(gol_a) or pd.isna(gol_b):
            continue

        gol_a = int(gol_a)
        gol_b = int(gol_b)

        # =========================================
        # TRAER PREDICCIONES
        # =========================================

        predicciones = pd.read_sql(
            '''
            SELECT *
            FROM predicciones
            WHERE partido_id = ?
            ''',
            conn,
            params=(partido_id,)
        )

        exactos = []

        # =========================================
        # VALIDAR PREDICCIONES
        # =========================================

        for _, pred in predicciones.iterrows():

            puntos = 0

            pred_a = pd.to_numeric(
                pred["pred_a"],
                errors="coerce"
            )

            pred_b = pd.to_numeric(
                pred["pred_b"],
                errors="coerce"
            )

            # IGNORAR DATOS VACÍOS
            if pd.isna(pred_a) or pd.isna(pred_b):
                continue

            pred_a = int(pred_a)
            pred_b = int(pred_b)

            # =========================================
            # MARCADOR EXACTO
            # =========================================

            if pred_a == gol_a and pred_b == gol_b:

                puntos = 3

                exactos.append(pred["id"])

            else:

                # =========================================
                # GANADOR CORRECTO
                # =========================================

                real = gol_a - gol_b
                prediccion = pred_a - pred_b

                if (
                    (real > 0 and prediccion > 0)
                    or
                    (real < 0 and prediccion < 0)
                    or
                    (real == 0 and prediccion == 0)
                ):

                    puntos = 1

            # =========================================
            # GUARDAR PUNTOS
            # =========================================

            cursor.execute(
                '''
                UPDATE predicciones
                SET puntos = ?
                WHERE id = ?
                ''',
                (
                    puntos,
                    pred["id"]
                )
            )

        conn.commit()

        # =========================================
        # BONUS MARCADOR ÚNICO
        # =========================================

        if len(exactos) == 1:

            cursor.execute(
                '''
                UPDATE predicciones
                SET puntos = puntos + 2
                WHERE id = ?
                ''',
                (exactos[0],)
            )

            conn.commit()

    conn.close()

# =========================================
# TABLA GENERAL
# =========================================

def tabla_general():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    tabla = pd.read_sql(
        '''
        SELECT
            usuario,
            SUM(puntos) AS puntos
        FROM predicciones
        GROUP BY usuario
        ORDER BY puntos DESC
        ''',
        conn
    )

    conn.close()

    return tabla