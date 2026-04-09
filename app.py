from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
import database  # Para inicializar las tablas
from models.pacientes import Paciente
from models.citas import Cita
from models.usuario import Usuario
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# No necesitamos init_db con SQLAlchemy

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro_paciente():
    if request.method == 'POST':
        documento = request.form['documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form.get('telefono')
        correo = request.form['correo']
        eps = request.form.get('eps')

        if Paciente.query_filter_by(documento=documento):
            flash('Documento ya existe', 'danger')
            return redirect(url_for('registro_paciente'))

        paciente = Paciente(documento=documento, nombre=nombre, apellido=apellido,
                            telefono=telefono, correo=correo, eps=eps)
        paciente.save()
        flash('Paciente registrado con éxito', 'success')
        return redirect(url_for('index'))

    return render_template('registro_paciente.html')

@app.route('/reservar', methods=['GET', 'POST'])
def reservar_cita():
    if request.method == 'POST':
        documento = request.form['documento']
        medico = request.form.get('medico')
        tipo_cita = request.form.get('tipo_cita')
        fecha = request.form['fecha']
        hora = request.form['hora']
        direccion_eps = request.form.get('direccion_eps')

        paciente = Paciente.query_filter_by(documento=documento)
        if not paciente:
            flash('Paciente no encontrado', 'danger')
            return redirect(url_for('reservar_cita'))

        cita = Cita(documento=documento, medico=medico, tipo_cita=tipo_cita,
                    fecha=fecha, hora=hora, direccion_eps=direccion_eps)
        cita.save()
        flash('Cita reservada con éxito', 'success')
        return redirect(url_for('index'))

    return render_template('reservar_cita.html')

@app.route('/consulta', methods=['GET'])
def consulta_cita():
    cita = None
    if 'id' in request.args:
        cita_id = request.args.get('id')
        cita = Cita.query_get(cita_id)
    return render_template('consulta_cita.html', cita=cita)

@app.route('/resultado')
def resultado_cita():
    return render_template('resultado_cita.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        usuario = Usuario.query_filter_by(correo=correo)
        if usuario and usuario.check_password(contraseña):
            session['usuario_id'] = usuario.id
            session['usuario_rol'] = usuario.rol
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        correo = request.form['correo']
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        rol = request.form['rol']

        if Usuario.query_filter_by(correo=correo):
            flash('Correo ya registrado', 'danger')
            return redirect(url_for('registro_usuario'))

        usuario = Usuario(correo=correo, nombre=nombre, rol=rol)
        usuario.set_password(contraseña)
        usuario.save()
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('registro_usuario.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_rol', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
