from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db():
    from models import Empleado, Conversacion
    db.create_all()

    # Cargar datos si la tabla está vacía
    if not Empleado.query.first():
        empleados = [
            Empleado(nombre="Juan Pérez", vacaciones=20, sueldo=1800000, antiguedad=2, fecha_ingreso="2022-01-10"),
            Empleado(nombre="María López", vacaciones=25, sueldo=1500000, antiguedad=3, fecha_ingreso="2021-05-20"),
            Empleado(nombre="Carlos Gómez", vacaciones=15, sueldo=1200000, antiguedad=1, fecha_ingreso="2023-02-01"),
        ]
        db.session.add_all(empleados)
        db.session.commit()