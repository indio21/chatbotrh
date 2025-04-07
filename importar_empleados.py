import pandas as pd
from models import Empleado, db
from datetime import datetime
from app import app

with app.app_context():
    df = pd.read_excel("empleados.xlsx")

    # Limpiar y normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    print("📋 Columnas normalizadas:", df.columns.tolist())

    df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], errors="coerce").dt.date

    for _, row in df.iterrows():
        if not Empleado.query.filter_by(email=row["email"]).first():
            nuevo_empleado = Empleado(
                nombre=row["nombre"],
                vacaciones=row["vacaciones"],
                sueldo=row["sueldo"],
                antiguedad=row["antiguedad"],
                fecha_ingreso=row["fecha_ingreso"],
                sanciones=row["sanciones"],
                referencias=row["referencias"]
            )
            db.session.add(nuevo_empleado)