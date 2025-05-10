from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

def init_db():
    from models import Empleado, Conversacion
    db.create_all()

  