from werkzeug.security import generate_password_hash
from app import app, db
from models import UsuarioRRHH

# Creamos un usuario de RRHH permanente
with app.app_context():
    if not UsuarioRRHH.query.filter_by(email="admin@empresa.com").first():
        nuevo_usuario = UsuarioRRHH(
            email="admin@empresa.com",
            password=generate_password_hash("admin123", method="scrypt")
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        print("✅ Usuario RRHH creado: admin@empresa.com / admin123")
    else:
        print("ℹ️ El usuario ya existe.")