import telebot
import json
import datetime
import os

# Archivo JSON para almacenar la información de los proyectos
proyectos_file = 'db/proyectos.json'
proyectos_folder = 'db/proyectos/'
# Manejar el comando /newproject
def np_command(bot, message):
    bot.reply_to(message, "¡Bienvenido al asistente de creación de proyectos! 📂\n\nPor favor, proporciona el nombre del proyecto:")

    # Registrar el siguiente paso de la conversación para obtener el nombre del proyecto
    bot.register_next_step_handler(message, get_project_name, bot)

def get_project_name(message, bot):
    project_name = message.text

    # Preguntar si el proyecto es público o privado
    bot.reply_to(message, f"Elige la visibilidad del proyecto:\n\n1. Público\n2. Privado")
    bot.register_next_step_handler(message, get_project_visibility, project_name, bot)

def get_project_visibility(message, project_name, bot):
    visibility = message.text.lower()

    if visibility == 'público' or visibility == 'publico' or visibility == '1':
        visibility = 'Público'
        # No se necesita clave para proyectos públicos
        key = None
    elif visibility == 'privado' or visibility == '2':
        visibility = 'Privado'
        # Solicitar al usuario que establezca una clave para el proyecto privado
        bot.reply_to(message, "Por favor, establece una clave para acceder al proyecto privado:")
        bot.register_next_step_handler(message, get_project_key, project_name, bot)
        return
    else:
        bot.reply_to(message, "Opción no válida. Por favor, elige entre 'Público' o 'Privado'.")
        return

    # Solicitar al usuario que envíe el archivo del proyecto
    bot.reply_to(message, f"El proyecto '{project_name}' es {visibility}. Ahora, por favor, envía el archivo del proyecto:")

    # Registrar el siguiente paso de la conversación para obtener el archivo del proyecto
    bot.register_next_step_handler(message, get_project_file, project_name, visibility, key, bot)

def get_project_key(message, project_name, bot):
    key = message.text

    # Solicitar al usuario que envíe el archivo del proyecto
    bot.reply_to(message, f"El proyecto '{project_name}' es privado y requiere clave. Por favor, envía el archivo del proyecto:")

    # Registrar el siguiente paso de la conversación para obtener el archivo del proyecto
    bot.register_next_step_handler(message, get_project_file, project_name, 'Privado', key, bot)

def get_project_file(message, project_name, visibility, key, bot):
    # Verificar si el usuario ha enviado un archivo
    if message.document is None:
        bot.reply_to(message, "No se envió un archivo. Por favor, envía el archivo del proyecto.")
        return

    # Obtener información del archivo del proyecto
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path

    # Descargar el archivo del proyecto
    file_content = bot.download_file(file_path)

    # Crear la carpeta "proyectos" si no existe
    if not os.path.exists(proyectos_folder):
        os.makedirs(proyectos_folder)

    # Obtener el nombre original del archivo
    file_name = message.document.file_name

    # Guardar el archivo en la carpeta "proyectos"
    with open(os.path.join(proyectos_folder, file_name), "wb") as f:
        f.write(file_content)

    # Solicitar al usuario que proporcione notas sobre la versión del proyecto
    bot.reply_to(message, "Por favor, proporciona unas notas sobre esta versión del proyecto:")
    bot.register_next_step_handler(message, save_project_info, project_name, visibility, key, file_name, bot)

def save_project_info(message, project_name, visibility, key, file_name, bot):
    # Verificar si el usuario envió notas sobre la versión del proyecto
    if not message.text:
        bot.reply_to(message, "No se proporcionaron notas sobre la versión del proyecto. Por favor, envía unas notas.")
        return

    # Obtener información adicional del usuario
    update_notes = message.text

    # Obtener la fecha y hora actual
    current_datetime = datetime.datetime.now()

    # Obtener información del usuario que envió el mensaje
    user_id = message.from_user.id

    # Crear un diccionario con la información del proyecto
    project_info = {
        "name": project_name,
        "visibility": visibility,
        "key": key,
        "file_name": file_name,
        "upload_date": str(current_datetime),
        "user_id": user_id,
        "update_notes": update_notes
    }

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Agregar el nuevo proyecto al diccionario
    proyectos_data.append(project_info)

    # Guardar datos de proyectos en el archivo
    with open(proyectos_file, 'w') as f:
        json.dump(proyectos_data, f)

    bot.reply_to(message, f"El proyecto '{project_name}' ha sido registrado exitosamente. ¡Gracias por compartirlo!")

# Manejar el comando /pl (project list)

def pl_command(bot, message):
    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Filtrar proyectos con visibilidad pública
    proyectos_publicos = [proyecto for proyecto in proyectos_data if proyecto["visibility"] == "Público"]

    if not proyectos_publicos:
        bot.reply_to(message, "No hay proyectos públicos registrados en este momento.")
        return

    # Crear un mensaje con la lista de proyectos públicos
    lista_proyectos = "Lista de proyectos públicos:\n\n"
    for proyecto in proyectos_publicos:
        lista_proyectos += f"📂 {proyecto['name']}\n"
    
    bot.reply_to(message, lista_proyectos)
# Manejar el comando /sp (save project)

def sp_command(bot, message):
    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Filtrar proyectos con visibilidad pública
    proyectos_publicos = [proyecto for proyecto in proyectos_data if proyecto["visibility"] == "Público"]

    if not proyectos_publicos:
        bot.reply_to(message, "No hay proyectos públicos registrados en este momento.")
        return

    # Crear un mensaje con la lista de proyectos públicos
    lista_proyectos = "Lista de proyectos públicos:\n\n"
    for proyecto in proyectos_publicos:
        lista_proyectos += f"📂 {proyecto['name']}\n"

    # Enviar la lista de proyectos públicos al usuario
    bot.reply_to(message, lista_proyectos)
    bot.reply_to(message, "Por favor, envía el nombre del proyecto que deseas guardar o envía 'cancelar' para cancelar la operación.")

    # Registrar el siguiente paso de la conversación para obtener el nombre del proyecto a guardar
    bot.register_next_step_handler(message, save_project, bot)

def save_project(message, bot):
    project_name = message.text.lower()

    # Verificar si el usuario envió 'cancelar'
    if project_name == 'cancelar':
        bot.reply_to(message, "Operación cancelada.")
        return

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Buscar el proyecto en la lista de proyectos públicos
    project_info = next((proyecto for proyecto in proyectos_data if proyecto["visibility"] == "Público" and proyecto["name"].lower() == project_name), None)

    if not project_info:
        bot.reply_to(message, f"No se encontró un proyecto público con el nombre '{project_name}'.")
        return

    # Obtener la ruta completa del archivo
    file_path = os.path.join(proyectos_folder, project_info["file_name"])

    # Enviar el archivo al usuario
    bot.send_document(message.chat.id, open(file_path, "rb"))

# Manejar el comando /up (update project)

def up_command(bot, message):
    bot.reply_to(message, "Por favor, envía el nombre del proyecto que deseas actualizar:")

    # Registrar el siguiente paso de la conversación para obtener el nombre del proyecto a actualizar
    bot.register_next_step_handler(message, update_project, bot)

def update_project(message, bot):
    project_name = message.text.lower()

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Buscar el proyecto en la lista de proyectos públicos
    project_info = next((proyecto for proyecto in proyectos_data if proyecto["visibility"] == "Público" and proyecto["name"].lower() == project_name), None)

    if not project_info:
        bot.reply_to(message, f"No se encontró un proyecto público con el nombre '{project_name}'.")
        return

    # Verificar si el usuario fue el que subió originalmente el proyecto
    user_id = message.from_user.id
    if user_id != project_info["user_id"]:
        bot.reply_to(message, "No tienes permiso para actualizar este proyecto, ya que no lo subiste originalmente.")
        return

    # Solicitar al usuario un nuevo archivo para actualizar el proyecto
    bot.reply_to(message, "Por favor, envía el nuevo archivo del proyecto para actualizarlo:")

    # Registrar el siguiente paso de la conversación para obtener el nuevo archivo del proyecto
    bot.register_next_step_handler(message, save_updated_project, project_info, bot)

def save_updated_project(message, project_info, bot):
    # Verificar si el usuario envió un archivo
    if message.document is None:
        bot.reply_to(message, "No se envió un archivo. Por favor, envía el nuevo archivo del proyecto.")
        return

    # Obtener información del archivo del proyecto
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path

    # Descargar el archivo del proyecto
    file_content = bot.download_file(file_path)

    # Obtener la ruta completa del archivo anterior
    old_file_path = os.path.join(proyectos_folder, project_info["file_name"])

    # Eliminar el archivo anterior
    os.remove(old_file_path)

    # Obtener el nombre original del archivo
    file_name = message.document.file_name

    # Guardar el nuevo archivo en la carpeta "proyectos"
    with open(os.path.join(proyectos_folder, file_name), "wb") as f:
        f.write(file_content)

    # Obtener información adicional del usuario
    bot.reply_to(message, "Por favor, proporciona unas notas sobre esta actualización:")
    bot.register_next_step_handler(message, save_updated_project_info, project_info, file_name, bot)

def save_updated_project_info(message, project_info, file_name, bot):
    update_notes = message.text

    # Obtener la fecha y hora actual
    current_datetime = datetime.datetime.now()

    # Actualizar la información del proyecto con el nuevo archivo y la fecha actual
    project_info["file_name"] = file_name
    project_info["upload_date"] = str(current_datetime)
    project_info["update_notes"] = update_notes

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Buscar el proyecto en la lista de proyectos públicos y actualizarlo
    for index, proyecto in enumerate(proyectos_data):
        if proyecto["visibility"] == "Público" and proyecto["name"].lower() == project_info["name"].lower():
            proyectos_data[index] = project_info
            break

    # Guardar datos de proyectos en el archivo
    with open(proyectos_file, 'w') as f:
        json.dump(proyectos_data, f)

    bot.reply_to(message, f"El proyecto '{project_info['name']}' ha sido actualizado exitosamente. ¡Gracias por compartir la actualización!")

# Manejar el comando /pi (project info)

def pi_command(bot, message):
    bot.reply_to(message, "Por favor, envía el nombre del proyecto del que deseas obtener información:")

    # Registrar el siguiente paso de la conversación para obtener el nombre del proyecto a consultar
    bot.register_next_step_handler(message, get_project_info, bot)

def get_project_info(message, bot):
    project_name = message.text.lower()

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Buscar el proyecto en la lista de proyectos
    project_info = next((proyecto for proyecto in proyectos_data if proyecto["name"].lower() == project_name), None)

    if not project_info:
        bot.reply_to(message, f"No se encontró información sobre el proyecto '{project_name}'.")
        return

    # Obtener información del proyecto
    name = project_info["name"]
    visibility = project_info["visibility"]
    upload_date = project_info["upload_date"]
    update_notes = project_info["update_notes"]

    # Crear el mensaje con la información del proyecto
    info_message = f"Información del Proyecto:\n\n" \
                   f"Nombre: {name}\n" \
                   f"Visibilidad: {visibility}\n" \
                   f"Fecha de Subida: {upload_date}\n" \
                   f"Notas de la versión: {update_notes}"

    bot.reply_to(message, info_message)

# Manejar el comando /dp (delete project)

def dp_command(bot, message):
    bot.reply_to(message, "Por favor, envía el nombre del proyecto que deseas eliminar:")

    # Registrar el siguiente paso de la conversación para obtener el nombre del proyecto a eliminar
    bot.register_next_step_handler(message, confirm_delete_project, bot)

def confirm_delete_project(message, bot):
    project_name = message.text.lower()

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Buscar el proyecto en la lista de proyectos
    project_info = next((proyecto for proyecto in proyectos_data if proyecto["name"].lower() == project_name), None)

    if not project_info:
        bot.reply_to(message, f"No se encontró información sobre el proyecto '{project_name}'.")
        return

    # Obtener el ID del usuario que envió el mensaje
    user_id = message.from_user.id

    # Verificar si el usuario tiene permiso para eliminar el proyecto
    if user_id != project_info["user_id"]:
        bot.reply_to(message, "No tienes permiso para eliminar este proyecto, ya que no lo subiste originalmente.")
        return

    # Pedir confirmación para eliminar el proyecto
    bot.reply_to(message, f"¿Estás seguro de que deseas eliminar el proyecto '{project_name}'?\n\nEscribe 'sí' o 'no'.")

    # Registrar el siguiente paso de la conversación para obtener la confirmación del usuario
    bot.register_next_step_handler(message, delete_project, project_info, bot)

def delete_project(message, project_info, bot):
    confirmation = message.text.lower()

    if confirmation == "sí" or confirmation == "si":
        # Eliminar el proyecto de la lista de proyectos
        with open(proyectos_file, 'r') as f:
            proyectos_data = json.load(f)

        proyectos_data = [proyecto for proyecto in proyectos_data if proyecto["name"].lower() != project_info["name"].lower()]

        with open(proyectos_file, 'w') as f:
            json.dump(proyectos_data, f)

        # Eliminar el archivo asociado al proyecto
        file_path = os.path.join(proyectos_folder, project_info["file_name"])
        if os.path.exists(file_path):
            os.remove(file_path)

        bot.reply_to(message, f"El proyecto '{project_info['name']}' ha sido eliminado exitosamente.")
    else:
        bot.reply_to(message, "Operación cancelada. El proyecto no fue eliminado.")

# Manejar el comando /mp (my projects)

def mp_command(bot, message):
    # Obtener el ID del usuario que envió el mensaje
    user_id = message.from_user.id

    # Cargar datos de proyectos desde el archivo
    with open(proyectos_file, 'r') as f:
        proyectos_data = json.load(f)

    # Filtrar los proyectos que coinciden con el ID del usuario
    user_projects = [proyecto for proyecto in proyectos_data if proyecto["user_id"] == user_id]

    if not user_projects:
        bot.reply_to(message, "No tienes proyectos registrados en este momento.")
        return

    # Crear un mensaje con la lista de los proyectos del usuario
    lista_proyectos = "Tus proyectos:\n\n"
    for proyecto in user_projects:
        lista_proyectos += f"📂 {proyecto['name']}\n Visibilidad: {proyecto['visibility']}\n Clave: {proyecto['key']}\n\n"

    bot.reply_to(message, lista_proyectos)
