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

        if "vacaciones" in pregunta:
            return f"Tenés {empleado.vacaciones} días de vacaciones."
        elif "sueldo" in pregunta or "cobro" in pregunta:
            return f"Tu sueldo es de ${empleado.sueldo}."
        elif "antigüedad" in pregunta or "años" in pregunta:
            return f"Tenés {empleado.antiguedad} años de antigüedad."
        elif "ingreso" in pregunta or "entraste" in pregunta:
            return f"Ingresaste a la empresa el {empleado.fecha_ingreso}."
        else:
            return "Podés preguntarme sobre tus vacaciones, sueldo, antigüedad o fecha de ingreso."

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

                if "vacaciones" in pregunta:
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.vacaciones} días de vacaciones."
                elif "sueldo" in pregunta or "cobra" in pregunta:
                    return f"{mensaje_intro}{emp.nombre} tiene un sueldo de ${emp.sueldo}."
                elif "antigüedad" in pregunta or "años" in pregunta:
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.antiguedad} años de antigüedad."
                elif "ingreso" in pregunta:
                    return f"{mensaje_intro}{emp.nombre} ingresó el {emp.fecha_ingreso}."
                else:
                    return f"{mensaje_intro}Podés preguntarme sobre vacaciones, sueldo o antigüedad de {emp.nombre}."

        # Si no se menciona nombre pero hay uno en contexto anterior
        empleado_id_contexto = session.get('ultimo_empleado')
        if empleado_id_contexto:
            emp = Empleado.query.get(empleado_id_contexto)
            if emp:
                if "vacaciones" in pregunta:
                    return f"Entiendo que seguís hablando de {emp.nombre}. Tiene {emp.vacaciones} días de vacaciones."
                elif "sueldo" in pregunta or "cobra" in pregunta:
                    return f"Entiendo que seguís hablando de {emp.nombre}. Su sueldo es de ${emp.sueldo}."
                elif "antigüedad" in pregunta or "años" in pregunta:
                    return f"{emp.nombre} tiene {emp.antiguedad} años de antigüedad."
                elif "ingreso" in pregunta:
                    return f"Ingresó el {emp.fecha_ingreso}."

        return "No encontré a ese empleado. Asegurate de escribir bien su nombre."

    return "Podés preguntarme sobre tus vacaciones, sueldo, antigüedad o fecha de ingreso."

