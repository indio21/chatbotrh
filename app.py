from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
import uuid
import os
from db import db, init_db
from models import Empleado, UsuarioRRHH, Conversacion
from chat import get_chat_response

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Asegurar que la carpeta 'instance' exista y crear la base si no existe
basedir = os.path.abspath(os.path.dirname(__file__))
db_folder = os.path.join(basedir, 'instance')
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, 'empleados.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    init_db()

@app.route('/crear_admin_temporal')
def crear_admin_temporal():
    if UsuarioRRHH.query.filter_by(email="admin@talent.com").first():
        return "El usuario ya existe."

    nuevo = UsuarioRRHH(
        email="admin@talent.com",
        password=generate_password_hash("admin123")
    )
    db.session.add(nuevo)
    db.session.commit()
    return "✅ Usuario admin creado con éxito. Usá admin@talent.com / admin123"

@app.route('/crear_empleado_temporal')
def crear_empleado_temporal():
    if Empleado.query.filter_by(email="empleado@talent.com").first():
        return "El empleado ya existe."

    nuevo = Empleado(
        nombre="Empleado Admin",
        email="empleado@talent.com",
        password=generate_password_hash("empleado123"),
        vacaciones=20,
        sueldo=1800000,
        antiguedad=5,
        fecha_ingreso="2020-01-10"
    )
    db.session.add(nuevo)
    db.session.commit()
    return "✅ Empleado creado con éxito. Usá empleado@talent.com / empleado123"

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

@app.route("/login_empleado", methods=["GET", "POST"])
def login_empleado():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        empleado = Empleado.query.filter_by(email=email).first()

        if empleado and check_password_hash(empleado.password, password):
            session["empleado_id"] = empleado.id
            session["session_id"] = f"empleado_{empleado.id}"
            return redirect(url_for("empleado_chat"))
        else:
            flash("Usuario o contraseña incorrectos")

    return render_template("login_empleado.html")

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

    # Mensaje inicial si no hay mensajes aún
    if not mensajes:
        bienvenida = "Hola, sobre qué colaborador quieres información?"
        mensaje_inicial = Conversacion(remitente='bot', mensaje=bienvenida, session_id=session['session_id'], timestamp=datetime.now(timezone.utc))
        db.session.add(mensaje_inicial)
        db.session.commit()
        mensajes.append(mensaje_inicial)

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

    # Mensaje inicial si no hay mensajes aún
    if not mensajes:
        bienvenida = "Hola, que información necesitarías?"
        mensaje_inicial = Conversacion(remitente='bot', mensaje=bienvenida, session_id=session['session_id'], timestamp=datetime.now(timezone.utc))
        db.session.add(mensaje_inicial)
        db.session.commit()
        mensajes.append(mensaje_inicial)

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

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "usuario_rrhh" in session:
        autor_usuario = "rrhh"
        mensaje_inicial = {"autor": "ruby", "texto": "Hola, sobre qué colaborador quieres información?"}
    elif "empleado_id" in session:
        autor_usuario = "empleado"
        mensaje_inicial = {"autor": "ruby", "texto": "Hola, me dirías tu Nombre y Apellido? Gracias!"}
    else:
        return redirect(url_for("login_rrhh"))  # o a login_empleado si lo preferís

    # Inicialización de la conversación si no hay mensajes previos
    if "mensajes" not in session:
        session["mensajes"] = [mensaje_inicial]

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        # Acá va tu función real (por ahora una simulada)
        # respuesta = obtener_respuesta(mensaje, autor_usuario)
        respuesta = f"Respuesta simulada a: {mensaje}"

        session["mensajes"].append({"autor": "usuario", "texto": mensaje})
        session["mensajes"].append({"autor": "ruby", "texto": respuesta})

    return render_template("chat.html", mensajes=session["mensajes"])




if __name__ == '__main__':
    app.run(debug=True)
