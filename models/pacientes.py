from database import db

class Paciente:
    def __init__(self, id=None, documento=None, nombre=None, apellido=None, telefono=None, correo=None, eps=None):
        self.id = id
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.eps = eps

    @staticmethod
    def query_filter_by(**kwargs):
        if 'documento' in kwargs:
            row = db.fetchone("SELECT * FROM pacientes WHERE documento = ?", (kwargs['documento'],))
            if row:
                return Paciente(id=row[0], documento=row[1], nombre=row[2], apellido=row[3], telefono=row[4], correo=row[5], eps=row[6])
        return None

    def save(self):
        if self.id:
            db.execute("UPDATE pacientes SET documento = ?, nombre = ?, apellido = ?, telefono = ?, correo = ?, eps = ? WHERE id = ?",
                       (self.documento, self.nombre, self.apellido, self.telefono, self.correo, self.eps, self.id))
        else:
            cursor = db.execute("INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps) VALUES (?, ?, ?, ?, ?, ?)",
                                (self.documento, self.nombre, self.apellido, self.telefono, self.correo, self.eps))
            self.id = cursor.lastrowid

    def __repr__(self):
        return f'<Paciente {self.documento} {self.nombre}>'
