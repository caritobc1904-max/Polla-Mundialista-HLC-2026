import sqlite3

conn = sqlite3.connect('mundial.db', check_same_thread=False)
cursor = conn.cursor()

# USUARIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    password TEXT
)
''')

# PARTIDOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jornada TEXT,
    fecha TEXT,
    hora TEXT,
    equipo_a TEXT,
    equipo_b TEXT,
    bandera_a TEXT,
    bandera_b TEXT,
    gol_a INTEGER,
    gol_b INTEGER
)
''')

# PREDICCIONES
cursor.execute('''
CREATE TABLE IF NOT EXISTS predicciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    partido_id INTEGER,
    pred_a INTEGER,
    pred_b INTEGER,
    puntos INTEGER DEFAULT 0
)
''')

# GOLEADOR
cursor.execute('''
CREATE TABLE IF NOT EXISTS goleador_mundial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    goleador TEXT
)
''')

# GOLES JUGADORES
cursor.execute('''
CREATE TABLE IF NOT EXISTS goleadores_real (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jugador TEXT UNIQUE,
    goles INTEGER DEFAULT 0
)
''')

conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partido_id INTEGER,
    equipo_a TEXT,
    equipo_b TEXT,
    goles_a INTEGER,
    goles_b INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')