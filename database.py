import sqlite3

conn = sqlite3.connect('mundial.db', check_same_thread=False)
cursor = conn.cursor()

# Participantes
cursor.execute('''
CREATE TABLE IF NOT EXISTS participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE
)
''')

# Partidos
cursor.execute('''
CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    equipo_a TEXT,
    equipo_b TEXT,
    gol_a INTEGER,
    gol_b INTEGER
)
''')

# Predicciones
cursor.execute('''
CREATE TABLE IF NOT EXISTS predicciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participante TEXT,
    partido_id INTEGER,
    pred_a INTEGER,
    pred_b INTEGER
)
''')

conn.commit()