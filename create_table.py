import os
from libsql_client import Client

# Configura tu URL de Turso aquí
DATABASE_URL = os.environ.get('DATABASE_URL', 'libsql://tu-db-tu-org.turso.io?authToken=tu_token')

client = Client(DATABASE_URL)

# Crear tabla users
client.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    contraseña_hash TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")

print("Tabla 'users' creada exitosamente en Turso DB.")