import sqlite3
import pandas as pd
import os

# =========================================
# CONEXIÓN SEGURA
# =========================================

DB_PATH = os.path.join(os.path.dirname(__file__), "mundial.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# =========================================
# CALCULAR PUNTOS (VERSIÓN SEGURA)
# =========================================

def calcular_puntos():

    resultados = pd.read_sql(
        '''
        SELECT partido_id, goles_a, goles_b
        FROM resultados
        ''',
        conn
    )

    for _, resultado in resultados.iterrows():

        partido_id = int(resultado["partido_id"])
        gol_a = int(resultado["goles_a"])
        gol_b = int(resultado["goles_b"])

        predicciones = pd.read_sql(
            '''
            SELECT id, pred_a, pred_b
            FROM predicciones
            WHERE partido_id = ?
            ''',
            conn,
            params=(partido_id,)
        )

        for _, pred in predicciones.iterrows():

            puntos = 0

            pred_a = int(pred["pred_a"])
            pred_b = int(pred["pred_b"])

            # =========================
            # MARCADOR EXACTO
            # =========================
            if pred_a == gol_a and pred_b == gol_b:
                puntos = 3

            else:
                real = gol_a - gol_b
                prediccion = pred_a - pred_b

                if (
                    (real > 0 and prediccion > 0) or
                    (real < 0 and prediccion < 0) or
                    (real == 0 and prediccion == 0)
                ):
                    puntos = 1

            cursor.execute(
                '''
                UPDATE predicciones
                SET puntos = ?
                WHERE id = ?
                ''',
                (puntos, pred["id"])
            )

    conn.commit()

# =========================================
# TABLA GENERAL
# =========================================

def tabla_general():

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

    return tabla