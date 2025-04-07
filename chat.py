from flask import session
from models import Empleado
from db import db

def get_chat_response(user_input):
    pregunta = user_input.lower()
    empleado_id = session.get('empleado_id')

    # 👤 Modo empleado: responde con sus propios datos
    if empleado_id:
        empleado = Empleado.query.get(empleado_id)
        if not empleado:
            return "No pude encontrar tus datos en el sistema."

        if "vacaciones" in pregunta or "dias" in pregunta or "licencia" in pregunta or "días" in pregunta or "quedan" in pregunta:
            return f"Tenés {empleado.vacaciones} días de vacaciones."
        # elif "sueldo" in pregunta or "cobro" in pregunta:
        elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","plata","dinero","salario","cobré"]):
            return f"Tu sueldo es de ${empleado.sueldo}."
        # elif "antiguedad" in pregunta or "años" in pregunta:
        elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo"]):
            return f"Tenés {empleado.antiguedad} años de antigüedad."
        elif any(p in pregunta for p in ["ingreso", "entraste", "inicio", "empezaste","entré","ingrese","arranque"]):
            return f"Ingresaste a la empresa el {empleado.fecha_ingreso}."
        elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","trayectoria","observaciones"]):
            return f"Sus referencias laborales son: {empleado.referencias}."
        elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","sancion","sancionado"]):
            return f"Sus sanciones son: {empleado.sanciones}."
        elif "gremio" in pregunta or "gremial" in pregunta or "día gremial" in pregunta:
            return f"Se considera como 'Dia del Trabajador del Automor' los días 24 de Febrero."
        elif "mudanza" in pregunta or "permiso" in pregunta:
            return f"El establecimiento otorgará un (1) día de permiso pago al personal que deba mudarse de vivienda, con excepción de aquellos que vivan en hotel o pensión."
        else:
            return "Podés preguntarme sobre tus vacaciones, sueldo, antigüedad, fecha de ingreso, sanciones o referencias laborales"

    # 👨‍💼 Modo RRHH: intenta encontrar un empleado mencionado
    if session.get('usuario_rrhh'):
        empleados = Empleado.query.all()
        for emp in empleados:
            nombre_partes = emp.nombre.lower().split()
            if any(parte in pregunta for parte in nombre_partes):
                anterior_id = session.get('ultimo_empleado')
                session['ultimo_empleado'] = emp.id  # Guardar último mencionado
                cambio_empleado = anterior_id and anterior_id != emp.id
                mensaje_intro = f"Ahora hablando de {emp.nombre}. " if cambio_empleado else ""

                if "vacaciones" in pregunta or "dias" in pregunta or "licencia" in pregunta or "dispone" in pregunta or "días" in pregunta or "quedan" in pregunta:
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.vacaciones} días de vacaciones."
                elif "gremio" in pregunta or "gremial" in pregunta or "día gremial" in pregunta:
                    return f"Se considera como 'Dia del Trabajador del Automor' los días 24 de Febrero."
                elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","plata","dinero","cobra","salario","cobró"]):
                    return f"{mensaje_intro}{emp.nombre} tiene un sueldo de ${emp.sueldo}."
                elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo"]):
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.antiguedad} años de antigüedad." 
                elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","trayectoria","observaciones"]):
                    return f"Sus referencias laborales son: {emp.referencias}."
                elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","sancion","sancionado"]):
                    return f"Sus sanciones son: {emp.sanciones}."
                elif any(p in pregunta for p in ["ingreso", "entraste", "inicio", "empezaste","entré","ingrese","arranque","fecha"]):
                    return f"{mensaje_intro}{emp.nombre} ingresó el {emp.fecha_ingreso}."
                elif "mudanza" in pregunta or "permiso" in pregunta:
                    return f"El establecimiento otorgará un (1) día de permiso pago al personal que deba mudarse de vivienda, con excepción de aquellos que vivan en hotel o pensión."
                else:
                    return f"{mensaje_intro}Podés preguntarme sobre tus vacaciones, sueldo, antigüedad, fecha de ingreso, sanciones o referencias laborales de {emp.nombre}."

        # Si no se menciona nombre pero hay uno en contexto anterior
        empleado_id_contexto = session.get('ultimo_empleado')
        if empleado_id_contexto:
            emp = Empleado.query.get(empleado_id_contexto)
            if emp:
                if "vacaciones" in pregunta or "dias" in pregunta or "licencia" in pregunta or "días" in pregunta or "quedan" in pregunta:
                    return f"Entiendo que seguís hablando de {emp.nombre}. Tiene {emp.vacaciones} días de vacaciones."
                elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","plata","dinero","cobra","salario","cobró"]):
                    return f"Entiendo que seguís hablando de {emp.nombre}. Su sueldo es de ${emp.sueldo}."
                elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo"]):
                    return f"{emp.nombre} tiene {emp.antiguedad} años de antigüedad."
                elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","sancion","sancionado"]):
                    return f"Sus sanciones son: {emp.sanciones}."
                elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","trayectoria","observaciones"]):
                    return f"Sus referencias laborales son: {emp.referencias}."
                elif any(p in pregunta for p in ["ingreso", "entraste", "inicio", "empezaste","entré","ingrese","arranque","fecha"]):
                    return f"Ingresó el {emp.fecha_ingreso}."
                elif "gremio" in pregunta or "gremial" in pregunta or "día gremial" in pregunta:
                    return f"Se considera como 'Dia del Trabajador del Automor' los días 24 de Febrero."
                elif "mudanza" in pregunta:
                    return f"El establecimiento otorgará un (1) día de permiso pago al personal que deba mudarse de vivienda, con excepción de aquellos que vivan en hotel o pensión."

        return "No encontré a ese empleado. Asegurate de escribir bien su nombre."

    return "Podés preguntarme sobre tus vacaciones, sueldo, antigüedad, fecha de ingreso, sanciones o referencias laborales"

