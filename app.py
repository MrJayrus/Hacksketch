import json
import telebot
file_path = '../db/apps.json'
#/app
def app_command(bot, message):
    # Obtener nombre de la aplicación desde el mensaje
    if len(message.text.split(' ')) > 1:
        app_name = message.text.split(' ')[1]
    else:
        bot.reply_to(message, "Por favor, proporcione un nombre de aplicación válido después del comando /app.\nPor ejemplo:\n/app IPVCEDEMO\n\nPuede consultar las apps disponibles con el comando /list")
        return

    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Verificar si la aplicación existe
    if app_name not in app_data:
        bot.reply_to(message, f'No se encontró información sobre la aplicación {app_name}.')
        return

    # Obtener información de la aplicación
    app = app_data[app_name]
    version = app['version']
    upload_date = app['upload_date']
    download_link = app['download_link']
    info = app['info']
    username = app['username']
    
    # Responder al mensaje con la información de la aplicación
    bot.reply_to(message, f'Aplicación **{app_name}** \nVersión: {version} \nSubida el {upload_date} \n\nInformación adicional: \n{info} \n\n👉 [Descargar ahora]({download_link})\n\nPara postear una aplicación con este bot, use el comando /addapp', parse_mode='Markdown')

#/addapp
def addapp_command(bot, message):
    bot.reply_to(message, '¿Cuál es el nombre de la aplicación que desea registrar?\n\nRecuerde que no puede usar caracteres especiales ni espacios en blanco.')
    bot.register_next_step_handler(message, check_existing_appp, bot)


def check_existing_appp(message, bot):
    app_name = message.text
    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Verificar si el nombre de la aplicación ya está registrado
    if app_name in app_data:
        bot.reply_to(message, f'La aplicación {app_name} ya está registrada por otro usuario.')
        return

    bot.reply_to(message, '¿Cuál es la versión de la aplicación?')
    bot.register_next_step_handler(message, get_version, app_name, bot)

def get_version(message, app_name, bot):
    version = message.text
    bot.reply_to(message, '¿Cuál es la fecha de lanzamiento?\nEj: 10-01-2023')
    bot.register_next_step_handler(message, get_upload_date, app_name, version, bot)

def get_upload_date(message, app_name, version, bot):
    upload_date = message.text
    bot.reply_to(message, '¿Cuál es el enlace de descarga de la aplicación?')
    bot.register_next_step_handler(message, get_info, app_name, version, upload_date, bot)

def get_info(message, app_name, version, upload_date, bot):
    download_link = message.text  # Obtener enlace de descarga del usuario
    bot.reply_to(message, 'Agrega alguna información adicional, como los requisitos o el tamaño de la descarga o ambos.')
    bot.register_next_step_handler(message, get_username, app_name, version, upload_date, download_link, bot)

def get_username(message, app_name, version, upload_date, download_link, bot):
    info = message.text  # Obtener información adicional del usuario
    username = message.from_user.username  # Obtener nombre de usuario del usuario que envió el mensaje
    save_app(bot, message, app_name, version, upload_date, download_link, info)

def save_app(bot, message, app_name, version, upload_date, download_link, info):
    username = message.from_user.id  # Obtener nombre de usuario del usuario que envió el mensaje

    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Agregar nuevos datos de la aplicación al diccionario
    app_data[app_name] = {
        'version': version,
        'upload_date': upload_date,
        'download_link': download_link,
        'info': info,
        'username': username  # Agregar nombre de usuario a los datos de la aplicación
    }

    # Guardar datos de la aplicación en el archivo
    with open(file_path, 'w') as f:
        json.dump(app_data, f)

    bot.reply_to(message, f'Aplicación {app_name} registrada en nuestra base de datos.')
    
#/list
def list_command(bot, message):
    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Verificar si hay aplicaciones disponibles
    if not app_data:
        bot.reply_to(message, 'No hay aplicaciones guardadas.')
        return

    # Crear lista de nombres de aplicaciones
    app_names = list(app_data.keys())

    # Responder al mensaje con la lista de nombres de aplicaciones
    bot.reply_to(message, f'Proyectos registrados:\n\n {", ".join(app_names)} \n\nPara ver información sobre una aplicación, use el comando:\n"/app <aplicacion>"')
    
#/editapp
def editapp_command(bot, message):
    bot.reply_to(message, '¿Cuál es el nombre de la aplicación que desea editar?')
    bot.register_next_step_handler(message, check_existing_app, bot)

def check_existing_app(message, bot):
    app_name = message.text
    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Verificar si el nombre de la aplicación ya está registrado
    if app_name in app_data:
        # Obtener el nombre de usuario del usuario que envió el mensaje
        username = message.from_user.id

        # Verificar si el usuario está autorizado para editar la aplicación
        if app_data[app_name]['username'] != username:
            bot.reply_to(message, 'Lo siento, no estás autorizado para editar esta aplicación.')
            return

        # Pedir al usuario la nueva versión de la aplicación
        bot.reply_to(message, 'Ingrese la nueva versión de la aplicación:')
        bot.register_next_step_handler(message, update_version, app_name, bot)
    else:
        bot.reply_to(message, f'La aplicación {app_name} no está registrada.')

def update_version(message, app_name, bot):
    version = message.text
    # Pedir al usuario la nueva fecha de lanzamiento de la aplicación
    bot.reply_to(message, 'Ingrese la nueva fecha de lanzamiento de la aplicación (Ej: 10-01-2023):')
    bot.register_next_step_handler(message, update_upload_date, app_name, version, bot)

def update_upload_date(message, app_name, version, bot):
    upload_date = message.text
    # Pedir al usuario el nuevo enlace de descarga de la aplicación
    bot.reply_to(message, 'Ingrese el nuevo enlace de descarga de la aplicación:')
    bot.register_next_step_handler(message, update_download_link, app_name, version, upload_date, bot)

def update_download_link(message, app_name, version, upload_date, bot):
    download_link = message.text
    # Pedir al usuario la nueva información adicional de la aplicación
    bot.reply_to(message, 'Ingrese la nueva información adicional de la aplicación:')
    bot.register_next_step_handler(message, update_info, app_name, version, upload_date, download_link, bot)

def update_info(message, app_name, version, upload_date, download_link, bot):
    info = message.text
    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Actualizar los datos de la aplicación en los datos
    app_data[app_name]['version'] = version
    app_data[app_name]['upload_date'] = upload_date
    app_data[app_name]['download_link'] = download_link
    app_data[app_name]['info'] = info

    # Guardar los datos actualizados en el archivo
    with open(file_path, 'w') as f:
        json.dump(app_data, f)

    bot.reply_to(message, f'Los datos de la aplicación {app_name} han sido actualizados.')
    
# /deleteapp
def deleteapp_command(bot, message):
    # Obtener nombre de la aplicación desde el mensaje
    if len(message.text.split(' ')) > 1:
        app_name = message.text.split(' ')[1]
    else:
        bot.reply_to(message, "Por favor, proporcione un nombre de aplicación válido después del comando /deleteapp.\nPor ejemplo:\n/deleteapp IPVCEDEMO")
        return

    # Cargar datos de aplicaciones desde el archivo
    with open(file_path, 'r') as f:
        app_data = json.load(f)

    # Verificar si la aplicación existe
    if app_name not in app_data:
        bot.reply_to(message, f'No se encontró información sobre la aplicación {app_name}.')
        return

    # Obtener el nombre de usuario del usuario que envió el mensaje
    username = message.from_user.id

    # Verificar si el usuario está autorizado para eliminar la aplicación
    if app_data[app_name]['username'] != username:
        bot.reply_to(message, 'Lo siento, no estás autorizado para eliminar esta aplicación.')
        return

    # Preguntar al usuario si realmente desea eliminar la aplicación
    confirmation_message = f"¿Estás seguro de que deseas eliminar la aplicación {app_name}? (si/no)"
    bot.reply_to(message, confirmation_message)
    bot.register_next_step_handler(message, confirm_deleteapp, app_name, app_data, bot)

def confirm_deleteapp(message, app_name, app_data, bot):
    confirmation = message.text.lower()
    if confirmation == 'si':
        # Eliminar la aplicación de los datos
        del app_data[app_name]

        # Guardar los datos actualizados en el archivo
        with open(file_path, 'w') as f:
            json.dump(app_data, f)

        bot.reply_to(message, f'Aplicación {app_name} eliminada de la base de datos.')
    elif confirmation == 'no':
        bot.reply_to(message, f'La aplicación {app_name} no ha sido eliminada.')
    else:
        bot.reply_to(message, 'Respuesta inválida. Por favor, responde con "si" o "no".')
        
