from app import app
from models import db, Empleado
from werkzeug.security import generate_password_hash
from datetime import date

with app.app_context():
    # Datos del nuevo empleado
    nombre = "Carlos"
    email = "carlos@empresa.com"
    password_plana = "carlos123"
    vacaciones = 10
    sueldo = 50000
    antiguedad = 2
    fecha_ingreso = date(2022, 6, 15)
    sanciones = "Ninguna"
    referencias = "Buena conducta y compromiso"

    # Verificar si ya existe
    if Empleado.query.filter_by(email=email).first():
        print("⚠️ El empleado ya existe.")
    else:
        nuevo_empleado = Empleado(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password_plana),
            vacaciones=vacaciones,
            sueldo=sueldo,
            antiguedad=antiguedad,
            fecha_ingreso=fecha_ingreso,
            sanciones=sanciones,
            referencias=referencias
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        print(f"✅ Empleado creado: {email}")
