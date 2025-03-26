from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
import uuid
import os
from db import db, init_db
from models import Empleado, UsuarioRRHH, Conversacion
from chat import get_chat_response

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_segura"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'empleados.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    init_db()

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/login_rrhh', methods=['GET', 'POST'])
def login_rrhh():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = UsuarioRRHH.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.password, password):
            session['usuario_rrhh'] = usuario.email
            session['session_id'] = str(uuid.uuid4())
            return redirect(url_for('chat_rrhh'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login_rrhh.html')

@app.route('/login_empleado', methods=['GET', 'POST'])
def login_empleado():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        empleado = Empleado.query.filter_by(email=email).first()
        if empleado and check_password_hash(empleado.password, password):
            session['empleado_id'] = empleado.id
            session['session_id'] = str(uuid.uuid4())
            return redirect(url_for('empleado_chat'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login_empleado.html')

@app.route('/chat_rrhh', methods=['GET', 'POST'])
def chat_rrhh():
    if 'usuario_rrhh' not in session:
        return redirect(url_for('login_rrhh'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_chat_response(user_input)

        db.session.add_all([
            Conversacion(remitente='usuario', mensaje=user_input, session_id=session['session_id'], timestamp=datetime.now(timezone.utc)),
            Conversacion(remitente='bot', mensaje=response, session_id=session['session_id'], timestamp=datetime.now(timezone.utc))
        ])
        db.session.commit()
        return redirect(url_for('chat_rrhh'))

    mensajes = Conversacion.query.filter_by(session_id=session['session_id']).order_by(Conversacion.timestamp.asc()).all()
    return render_template('index.html', mensajes=mensajes)

@app.route('/empleado_chat', methods=['GET', 'POST'])
def empleado_chat():
    if 'empleado_id' not in session:
        return redirect(url_for('login_empleado'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_chat_response(user_input)

        db.session.add_all([
            Conversacion(remitente='usuario', mensaje=user_input, session_id=session['session_id'], timestamp=datetime.now(timezone.utc)),
            Conversacion(remitente='bot', mensaje=response, session_id=session['session_id'], timestamp=datetime.now(timezone.utc))
        ])
        db.session.commit()
        return redirect(url_for('empleado_chat'))

    mensajes = Conversacion.query.filter_by(session_id=session['session_id']).order_by(Conversacion.timestamp.asc()).all()
    empleado = Empleado.query.get(session['empleado_id'])
    return render_template('index.html', mensajes=mensajes, empleado=empleado)

@app.route('/reiniciar')
def reiniciar():
    session['session_id'] = str(uuid.uuid4())
    return redirect(request.referrer or url_for('inicio'))

@app.route('/logout_rrhh')
def logout_rrhh():
    session.pop('usuario_rrhh', None)
    session.pop('session_id', None)
    return redirect(url_for('inicio'))

@app.route('/logout_empleado')
def logout_empleado():
    session.pop('empleado_id', None)
    session.pop('session_id', None)
    return redirect(url_for('inicio'))

@app.route('/historial')
def historial():
    if 'usuario_rrhh' not in session:
        return redirect(url_for('login_rrhh'))
    mensajes = Conversacion.query.filter_by(session_id=session['session_id']).order_by(Conversacion.timestamp.asc()).all()
    return render_template('historial.html', mensajes=mensajes)

@app.route('/historial_empleado')
def historial_empleado():
    if 'empleado_id' not in session:
        return redirect(url_for('login_empleado'))
    mensajes = Conversacion.query.filter_by(session_id=session['session_id']).order_by(Conversacion.timestamp.asc()).all()
    return render_template('historial_empleado.html', mensajes=mensajes)

if __name__ == '__main__':
    app.run(debug=True)
