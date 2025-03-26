from werkzeug.security import generate_password_hash
from app import app, db
from models import Empleado

# Ingreso de datos
nombre = input("👤 Nombre completo del empleado: ")
email = input("📧 Correo electrónico: ")
password = input("🔐 Contraseña: ")
vacaciones = int(input("🏖️ Días de vacaciones: "))
sueldo = int(input("💰 Sueldo: "))
antiguedad = int(input("📅 Años de antigüedad: "))
fecha_ingreso = input("🗓️ Fecha de ingreso (YYYY-MM-DD): ")

hashed_password = generate_password_hash(password)

with app.app_context():
    if Empleado.query.filter_by(email=email).first():
        print("❌ Ya existe un empleado con ese email.")
    else:
        nuevo = Empleado(
            nombre=nombre,
            email=email,
            password=hashed_password,
            vacaciones=vacaciones,
            sueldo=sueldo,
            antiguedad=antiguedad,
            fecha_ingreso=fecha_ingreso
        )
        db.session.add(nuevo)
        db.session.commit()
        print("✅ Empleado creado correctamente.")
