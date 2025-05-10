from db import db
from datetime import datetime, timezone

class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))  # contraseña hasheada
    fecha_ingreso = db.Column(db.String(20), nullable=True)
    antiguedad = db.Column(db.Integer, nullable=True)
    vacaciones = db.Column(db.Integer, nullable=False)
    pendientes = db.Column(db.Integer, nullable=True)
    sueldo = db.Column(db.Integer, nullable=False)
    puesto = db.Column(db.String(100), nullable=False)
    sanciones = db.Column(db.Text, nullable=True)  # ✅ NUEVO CAMPO
    referencias = db.Column(db.Text, nullable=True)  # ✅ NUEVO CAMPO
    trayectoria = db.Column(db.Text, nullable=True)  # ✅ NUEVO CAMPO
    cursos = db.Column(db.Text, nullable=True)  # ✅ NUEVO CAMPO
    

class UsuarioRRHH(db.Model):
    __tablename__ = "usuarios_rrhh"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # contraseña hasheada

class Conversacion(db.Model):
    __tablename__ = "conversaciones"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(32), nullable=False)
    remitente = db.Column(db.String(10))  # "usuario" o "bot"
    mensaje = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

