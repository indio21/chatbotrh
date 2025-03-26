from werkzeug.security import generate_password_hash
from app import app, db
from models import UsuarioRRHH

# Datos del nuevo usuario
email = input("📧 Ingresá el email del usuario RRHH: ")
password = input("🔐 Ingresá la contraseña: ")

hashed_password = generate_password_hash(password)

with app.app_context():
    if UsuarioRRHH.query.filter_by(email=email).first():
        print("❌ Ya existe un usuario con ese email.")
    else:
        nuevo_usuario = UsuarioRRHH(email=email, password=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        print("✅ Usuario RRHH creado correctamente.")
