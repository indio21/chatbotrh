from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

db = SQLAlchemy()


def init_db():
    from models import Empleado, Conversacion
    db.create_all()

    # Cargar datos iniciales si está vacío
    if not Empleado.query.first():
        empleados_base = [
            Empleado(nombre="Juan Pérez", vacaciones=20, sueldo=1800000, antiguedad=2, fecha_ingreso="2022-01-10",sanciones="No presenta",referencias="Muy buenas, referencias positivas."),
            Empleado(nombre="María López", vacaciones=25, sueldo=1500000, antiguedad=3, fecha_ingreso="2021-05-20",sanciones="No presenta",referencias="Muy buenas, referencias positivas."),
            Empleado(nombre="Luciana Astudillo", vacaciones=21, sueldo=1308707, antiguedad=5, fecha_ingreso="10/02/2020",sanciones="No presenta",referencias="Muy buenas, referencias positivas."),
            Empleado(nombre="Martina Lázaro", vacaciones=28, sueldo=1754658, antiguedad=11, fecha_ingreso="1/12/2013",sanciones="No presenta",referencias="Muy buenas, referencias positivas."),
            Empleado(nombre="Érica Martínez", vacaciones=28, sueldo=1857060, antiguedad=18, fecha_ingreso="15/6/2006",sanciones="No presenta",referencias="Muy buenas, referencias positivas.")
        ]
        db.session.add_all(empleados_base)


