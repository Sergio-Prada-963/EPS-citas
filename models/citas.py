from database import db
from models.pacientes import Paciente

class Cita:
    def __init__(self, id=None, documento=None, medico=None, tipo_cita=None, fecha=None, hora=None, direccion_eps=None):
        self.id = id
        self.documento = documento
        self.medico = medico
        self.tipo_cita = tipo_cita
        self.fecha = fecha
        self.hora = hora
        self.direccion_eps = direccion_eps

    @staticmethod
    def query_get(id):
        row = db.fetchone("SELECT * FROM citas WHERE id = ?", (id,))
        if row:
            return Cita(id=row[0], documento=row[1], medico=row[2], tipo_cita=row[3], fecha=row[4], hora=row[5], direccion_eps=row[6])
        return None

    def save(self):
        if self.id:
            db.execute("UPDATE citas SET documento = ?, medico = ?, tipo_cita = ?, fecha = ?, hora = ?, direccion_eps = ? WHERE id = ?",
                       (self.documento, self.medico, self.tipo_cita, self.fecha, self.hora, self.direccion_eps, self.id))
        else:
            cursor = db.execute("INSERT INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps) VALUES (?, ?, ?, ?, ?, ?)",
                                (self.documento, self.medico, self.tipo_cita, self.fecha, self.hora, self.direccion_eps))
            self.id = cursor.lastrowid

    def __repr__(self):
        return f'<Cita {self.id} {self.fecha} {self.hora}>'
