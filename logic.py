import sqlite3
import pandas as pd

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# ==================================
# CALCULAR PUNTOS
# ==================================

def calcular_puntos():

    # RESETEAR PUNTOS
    cursor.execute(
        '''
        UPDATE predicciones
        SET puntos = 0
        '''
    )

    conn.commit()

    # OBTENER PARTIDOS
    partidos = pd.read_sql(
        '''
        SELECT *
        FROM partidos
        WHERE gol_a IS NOT NULL
        AND gol_b IS NOT NULL
        ''',
        conn
    )

    # RECORRER PARTIDOS
    for _, partido in partidos.iterrows():

        predicciones = pd.read_sql(
            f'''
            SELECT *
            FROM predicciones
            WHERE partido_id = {partido["id"]}
            ''',
            conn
        )

        exactos = []

        # ==========================
        # VALIDAR PREDICCIONES
        # ==========================

        for _, pred in predicciones.iterrows():

            puntos = 0

            # MARCADOR EXACTO
            if (
                pred['pred_a'] == partido['gol_a']
                and
                pred['pred_b'] == partido['gol_b']
            ):

                puntos = 3

                exactos.append(pred['id'])

            else:

                # GANADOR CORRECTO

                real = (
                    partido['gol_a']
                    -
                    partido['gol_b']
                )

                prediccion = (
                    pred['pred_a']
                    -
                    pred['pred_b']
                )

                if (
                    (real > 0 and prediccion > 0)
                    or
                    (real < 0 and prediccion < 0)
                    or
                    (real == 0 and prediccion == 0)
                ):

                    puntos = 1

            # GUARDAR PUNTOS
            cursor.execute(
                '''
                UPDATE predicciones
                SET puntos=?
                WHERE id=?
                ''',
                (
                    puntos,
                    pred['id']
                )
            )

        conn.commit()

        # ==========================
        # BONUS UNICO
        # ==========================

        if len(exactos) == 1:

            exacto_id = exactos[0]

            cursor.execute(
                '''
                UPDATE predicciones
                SET puntos = puntos + 2
                WHERE id=?
                ''',
                (exacto_id,)
            )

            conn.commit()

# ==================================
# TABLA GENERAL
# ==================================

def tabla_general():

    tabla = pd.read_sql(
        '''
        SELECT
            usuario,
            SUM(puntos) as puntos
        FROM predicciones
        GROUP BY usuario
        ORDER BY puntos DESC
        ''',
        conn
    )

    return tabla