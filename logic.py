import sqlite3
import pandas as pd

conn = sqlite3.connect('mundial.db', check_same_thread=False)

def calcular_puntos(pred_a, pred_b, real_a, real_b, unicos):

    if pred_a == real_a and pred_b == real_b:
        puntos = 3

        if unicos == 1:
            puntos += 2

    elif (
        (pred_a > pred_b and real_a > real_b) or
        (pred_a < pred_b and real_a < real_b) or
        (pred_a == pred_b and real_a == real_b)
    ):
        puntos = 1

    else:
        puntos = 0

    return puntos


def tabla_general():

    partidos = pd.read_sql('SELECT * FROM partidos', conn)
    predicciones = pd.read_sql('SELECT * FROM predicciones', conn)

    resultados = []

    for _, pred in predicciones.iterrows():

        partido = partidos[partidos['id'] == pred['partido_id']]

        if partido.empty:
            continue

        partido = partido.iloc[0]

        if pd.isna(partido['gol_a']) or pd.isna(partido['gol_b']):
            continue

        unicos = len(predicciones[
            (predicciones['partido_id'] == pred['partido_id']) &
            (predicciones['pred_a'] == partido['gol_a']) &
            (predicciones['pred_b'] == partido['gol_b'])
        ])

        puntos = calcular_puntos(
            pred['pred_a'],
            pred['pred_b'],
            partido['gol_a'],
            partido['gol_b'],
            unicos
        )

        resultados.append({
            'participante': pred['participante'],
            'puntos': puntos
        })

    df = pd.DataFrame(resultados)

    if df.empty:
        return pd.DataFrame(columns=['participante', 'puntos'])

    tabla = df.groupby('participante')['puntos'].sum().reset_index()

    tabla = tabla.sort_values(by='puntos', ascending=False)

    return tabla