import sqlite3
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'eps_citas.db')

conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
cursor = conn.cursor()

# Crear tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    eps TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT NOT NULL,
    medico TEXT,
    tipo_cita TEXT,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    direccion_eps TEXT,
    FOREIGN KEY (documento) REFERENCES pacientes (documento)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    contraseña_hash TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")

conn.commit()

# Para usar en modelos
class DB:
    @staticmethod
    def execute(query, params=()):
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    @staticmethod
    def fetchone(query, params=()):
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    @staticmethod
    def fetchall(query, params=()):
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    @staticmethod
    def lastrowid():
        return cursor.lastrowid

db = DB()
