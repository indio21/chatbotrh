# Agregamos la línea al final del archivo 'chat.py'
file_path = "/mnt/data/chat.py"

# Leer el contenido actual
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Agregar alias si no está ya
if "obtener_respuesta" not in content:
    content += "\n\nobtener_respuesta = procesar_mensaje\n"

# Guardar el contenido modificado
with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)

"Archivo actualizado con alias 'obtener_respuesta'."
