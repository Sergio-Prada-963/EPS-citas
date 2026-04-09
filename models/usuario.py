from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id=None, correo=None, nombre=None, contraseña_hash=None, rol=None):
        self.id = id
        self.correo = correo
        self.nombre = nombre
        self.contraseña_hash = contraseña_hash
        self.rol = rol

    @staticmethod
    def query_filter_by(**kwargs):
        if 'correo' in kwargs:
            row = db.fetchone("SELECT * FROM users WHERE correo = ?", (kwargs['correo'],))
            if row:
                return Usuario(id=row[0], correo=row[1], nombre=row[2], contraseña_hash=row[3], rol=row[4])
        return None

    @staticmethod
    def query_get(id):
        row = db.fetchone("SELECT * FROM users WHERE id = ?", (id,))
        if row:
            return Usuario(id=row[0], correo=row[1], nombre=row[2], contraseña_hash=row[3], rol=row[4])
        return None

    def save(self):
        if self.id:
            db.execute("UPDATE users SET correo = ?, nombre = ?, contraseña_hash = ?, rol = ? WHERE id = ?",
                       (self.correo, self.nombre, self.contraseña_hash, self.rol, self.id))
        else:
            cursor = db.execute("INSERT INTO users (correo, nombre, contraseña_hash, rol) VALUES (?, ?, ?, ?)",
                                (self.correo, self.nombre, self.contraseña_hash, self.rol))
            self.id = cursor.lastrowid

    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'