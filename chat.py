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
        elif  any(p in pregunta for p in ["disponibles","pendientes","tomarme","dispongo","vacaciones","licencias"]): #dias diponibles de vacaciones
            return f"Por tu antigüedad, te corresponden {empleado.vacaciones} días de vacaciones. Tienes disponibles {empleado.pendientes} días de vacaciones ."
        elif any(p in pregunta for p in ["disponibles","pendientes","tomarme","dispongo"]): #dias diponibles de vacaciones
                    return f"Actualmente {empleado.nombre}, cuentas con {empleado.pendientes} días de vacaciones disponibles."
        elif any(p in pregunta for p in ["puesto","cargo","funcion","trabajo","puesto de trabajo","lugar"]): #puesto
            return f"Tu puesto actualmente es el de  {empleado.puesto}."
        # elif "sueldo" in pregunta or "cobro" in pregunta:
        elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","renumeración","plata","dinero","salario","cobré"]):
            return f"Su renumeración es de ${empleado.sueldo}."
        # elif "antiguedad" in pregunta or "años" in pregunta:
        elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo","antigüedad"]):
            return f"{empleado.nombre}, tu antigüedad en la empresa es de {empleado.antiguedad} años."
        elif any(p in pregunta for p in ["ingreso", "entraste", "inicié","comencé", "empezaste","entré","ingrese","ingresé","arranqué"]):
            return f"{empleado.nombre}, ingresaste a la empresa el {empleado.fecha_ingreso}." #ingreso
        elif any(p in pregunta for p in ["cursos","curso","capacitación","capacitaciones","capacitacion","cursos realizados","formación","charlas","contenido"]): #cursos
            return f"Capacitaciones: {empleado.cursos}." if empleado.cursos else "Usted no registra cursos."
        elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","trayectoria","observaciones","legajo"]):
            return f"Sus referencias laborales son: {empleado.referencias}."
        elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","sancion","sanción","sancionado","suspensión"]):
            return f"Sus sanciones son: {empleado.sanciones}."
        elif any(p in pregunta for p in ["gremio","gremial","trabajador","sindicato","sindical"]):
            return f"Se considera como 'Día del Trabajador del Automotor' los días 24 de Febrero."
        elif any(p in pregunta for p in ["nacimiento","paternidad","maternidad","papá","mamá","hijo","nacido","bebé"]):
            return f"Por nacimiento de hijos/as: El personal masculino tendrá derecho a tres (3) días de licencia extraordinaria (Art. 7° Ley 18.338)."
        elif "mudanza" in pregunta or "domicilio" in pregunta or "mudo" in pregunta:
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

                if any(p in pregunta for p in ["disponibles","pendientes","tomarse","quedan","licencia","vacaciones","dispone"]): #dias diponibles de vacaciones
                    return f"A {emp.nombre}  con respecto a su antigüedad, le corresponden {emp.vacaciones} días de vacaciones y tiene disponibles {emp.pendientes} días de vacaciones."
                elif "gremio" in pregunta or "gremial" in pregunta or "sindicato" in pregunta or "automotor" in pregunta or "sindical" in pregunta: #dia gremial
                    return f"Se considera como 'Dia del Trabajador del Automotor' los días 24 de Febrero."      #sueldo
                elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","renumeración","plata","dinero","cobra","salario","cobró"]):
                    return f"La renumeración de {emp.nombre} actualmente es de ${emp.sueldo}."
                elif any(p in pregunta for p in ["puesto","cargo","funcion","trabajo","puesto de trabajo","lugar"]): #puesto
                    return f"{emp.nombre} es {emp.puesto} dentro de la empresa."
                elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo","antigüedad","ingreso","ingresó"]): #antiguedad
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.antiguedad} años de antigüedad. Ingresó el {emp.fecha_ingreso}." 
                elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","observaciones","observación","legajo"]):
                    if emp.referencias:     #referencias laborales
                        return f"{emp.nombre}: {emp.referencias}." if emp.referencias else "No registra referencias."
                elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","suspensión","sancion","sanción","sancionado","apercibimiento","apercibimientos"]): #sanciones
                    return f" {emp.nombre}: {emp.sanciones}." if emp.sanciones else "No registra sanciones."  
                elif any(p in pregunta for p in ["ingreso","ingresó", "entraste", "inicio", "empezaste","entré","ingrese","arranque","fecha","primer día"]):
                    return f"{mensaje_intro}{emp.nombre} ingresó el {emp.fecha_ingreso}." #ingreso
                elif any(p in pregunta for p in ["trayectoria","trayectorias","trayectoria laboral","camino","ascenso","ascensos","puestos que estuvo"]): #trayectoria
                    return f"Trayectoria: {emp.trayectoria}." if emp.trayectoria else "No registra trayectoria." #trayectoria
                elif any(p in pregunta for p in ["cursos","curso","capacitación","capacitaciones","cursos realizados","formación","charlas","contenido","capacitacion","formacion"]): #cursos
                    return f"Capacitaciones: {emp.cursos}." if emp.cursos else "No registra cursos."
                elif any(p in pregunta for p in ["mudanza","vivienda","mudo","domicilio"]): #cursos
                    return f"El establecimiento otorgará un (1) día de permiso pago al personal que deba mudarse de vivienda, con excepción de aquellos que vivan en hotel o pensión."
                elif any(p in pregunta for p in ["nacimiento","paternidad","maternidad","papá","mamá","hijo","nacido","bebé"]):
                    return f"Por nacimiento de hijos/as: El personal masculino tendrá derecho a tres (3) días de licencia extraordinaria (Art. 7° Ley 18.338)."
                else:
                    return f"{mensaje_intro}Podés preguntarme sobre vacaciones, días disponibles de vacaciones, puesto, sueldo, antigüedad, fecha de ingreso, sanciones, referencias laborales, trayectoria y cursos {emp.nombre}."

        # Si no se menciona nombre pero hay uno en contexto anterior
        empleado_id_contexto = session.get('ultimo_empleado')
        if empleado_id_contexto:
            emp = Empleado.query.get(empleado_id_contexto)
            if emp:
                if any(p in pregunta for p in ["disponibles","pendientes","tomarse","quedan","vacaciones","licencia","dispone"]): #dias diponibles de vacaciones
                    return f"Entiendo que sigues hablando de {emp.nombre}. {emp.nombre}  con respecto a su antigüedad, le corresponden {emp.vacaciones} días de vacaciones y tiene disponibles {emp.pendientes} días de vacaciones"
                elif "gremio" in pregunta or "gremial" in pregunta or "sindicato" in pregunta or "sindical" in pregunta: #dia gremial
                    return f"Se considera como 'Dia del Trabajador del Automotor' los días 24 de Febrero."      #sueldo
                elif any(p in pregunta for p in ["sueldo","cobro","renumeracion","renumeración","plata","dinero","cobra","salario","cobró"]):
                    return f"Entiendo que sigues hablando de {emp.nombre}. La renumeración de {emp.nombre} actualmente es de ${emp.sueldo}."
                elif any(p in pregunta for p in ["puesto","cargo","funcion","trabajo","puesto de trabajo","lugar"]): #puesto
                    return f"{emp.nombre} es {emp.puesto} dentro de la empresa."
                elif any(p in pregunta for p in ["antiguedad","tiempo","estoy","periodo","antigüedad","ingreso","ingresó"]): #antiguedad
                    return f"{mensaje_intro}{emp.nombre} tiene {emp.antiguedad} años de antigüedad. Ingresó el {emp.fecha_ingreso}." 
                elif any(p in pregunta for p in ["referencias","laborales","recomendaciones","referencia","observaciones","observación","legajo"]):
                    if emp.referencias:     #referencias laborales
                        return f"{emp.nombre}: {emp.referencias}." if emp.referencias else "No registra referencias."
                elif any(p in pregunta for p in ["sanciones","multas","suspendido","suspension","suspensión","sancion","sanción","sancionado","apercibimiento","apercibimientos"]): #sanciones
                    return f" {emp.nombre}: {emp.sanciones}." if emp.sanciones else "No registra sanciones."  
                elif any(p in pregunta for p in ["ingreso","ingresó", "entraste", "inicio", "empezaste","entré","ingrese","arranque","fecha","primer día"]):
                    return f"{mensaje_intro}{emp.nombre} ingresó el {emp.fecha_ingreso}." #ingreso
                elif any(p in pregunta for p in ["trayectoria","trayectorias","trayectoria laboral","camino","ascenso","ascensos","puestos que estuvo"]): #trayectoria
                    return f"Trayectoria: {emp.trayectoria}." if emp.trayectoria else "No registra trayectoria." #trayectoria
                elif any(p in pregunta for p in ["cursos","curso","capacitación","capacitaciones","cursos realizados","formación","charlas","contenido"]): #cursos
                    return f"Capacitaciones: {emp.cursos}." if emp.cursos else "No registra cursos."
                elif "mudanza" in pregunta or "permiso" in pregunta:    #permiso mudanza
                    return f"El establecimiento otorgará un (1) día de permiso pago al personal que deba mudarse de vivienda, con excepción de aquellos que vivan en hotel o pensión."
                elif any(p in pregunta for p in ["nacimiento","paternidad","maternidad","papá","mamá","hijo","nacido","bebé"]):
                    return f"Por nacimiento de hijos/as: El personal masculino tendrá derecho a tres (3) días de licencia extraordinaria (Art. 7° Ley 18.338)."
                else:
                    return f"{mensaje_intro}Podés preguntarme sobre vacaciones, días disponibles de vacaciones, puesto, sueldo, antigüedad, fecha de ingreso, sanciones, referencias laborales, trayectoria y cursos {emp.nombre}."

        return "No encontré a ese empleado. Asegurate de escribir bien su nombre."

    return "Podés preguntarme sobre tus vacaciones, sueldo, antigüedad, fecha de ingreso, sanciones o referencias laborales"

