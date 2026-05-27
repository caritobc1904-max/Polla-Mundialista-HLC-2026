import sqlite3
import pandas as pd

conn = sqlite3.connect(
    'mundial.db',
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================
# CALCULAR PUNTOS
# =========================================

def calcular_puntos():

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
        # LIMPIAR IDS CORRUPTOS
        # =========================================

        partido_id = pd.to_numeric(
            resultado["partido_id"],
            errors="coerce"
        )

        # SI EL ID ESTA DAÑADO LO IGNORA
        if pd.isna(partido_id):
            continue

        partido_id = int(partido_id)

        gol_a = int(resultado["goles_a"])
        gol_b = int(resultado["goles_b"])

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

            pred_a = int(pred["pred_a"])
            pred_b = int(pred["pred_b"])

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
        # BONUS UNICO
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

# =========================================
# TABLA GENERAL
# =========================================

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