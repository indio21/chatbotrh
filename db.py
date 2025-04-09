from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

def init_db():
    from models import Empleado, Conversacion
    db.create_all()

    # Cargar datos si la tabla está vacía
    if not Empleado.query.first():
        empleados = [
   Empleado(nombre="Juan Pérez", vacaciones=20, sueldo=1800000, antiguedad=2, fecha_ingreso="2022-01-10",sanciones="No presenta",referencias="Muy buenas, referencias positivas.", email="juan@talent.com",
        password=generate_password_hash("juan123")),
            Empleado(nombre="María López", vacaciones=25, sueldo=1500000, antiguedad=3, fecha_ingreso="2021-05-20",sanciones="No presenta",referencias="Positivas", email="maria@talent.com",
        password=generate_password_hash("maria123")),
            Empleado(nombre="Luciana Astudillo", vacaciones=21, sueldo=1308707, antiguedad=5, fecha_ingreso="10/02/2020",sanciones="No presenta",referencias="Muy buenas, referencias positivas.", email="luciana@talent.com",
        password=generate_password_hash("luciana123")),
            Empleado(nombre="Martina Lázaro", vacaciones=28, sueldo=1754658, antiguedad=11, fecha_ingreso="1/12/2013",sanciones="No presenta",referencias="Muy buenas, referencias positivas.", email="martina@talent.com",
        password=generate_password_hash("martina123")),
            Empleado(nombre="Érica Martínez", vacaciones=28, sueldo=1857060, antiguedad=18, fecha_ingreso="15/6/2006",sanciones="No presenta",referencias="Muy buenas, referencias positivas.", email="erica@talent.com",
        password=generate_password_hash("erica123")),
            Empleado(nombre="Damián Grosso", vacaciones=21, sueldo=1467800, antiguedad=7, fecha_ingreso="15/3/2018",sanciones="1 Sanción",referencias="Se trata de un colaborador cumplidor, responsable pero con reiterados llamados de atención por llegadas tardes injustificadas", email="damian@talent.com",
        password=generate_password_hash("damian123")),
            Empleado(nombre="Claudio Pereyra", vacaciones=14, sueldo=967890, antiguedad=0, fecha_ingreso="8/9/2024",sanciones="1 apercibimiento",referencias="Durante sus primeros meses de experiencia laboral, fue partícipe de un evento conflictivo y físico con un compañero. Lo que llevó a una sanción.",email="claudio@talent.com",
        password=generate_password_hash("claudio123")),
            Empleado(nombre="Mateo Fenoglio", vacaciones=28, sueldo=1790684, antiguedad=15, fecha_ingreso="7/8/2009",sanciones="No presenta",referencias="Muy buenas, referencias positiva.",email="mateo@talent.com",
        password=generate_password_hash("mateo123"))
        ]
        db.session.add_all(empleados)
        db.session.commit()