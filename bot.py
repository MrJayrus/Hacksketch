import telebot
import time
import threading
from functools import wraps
#from ads import *
from app import *
from projects import *
from basics import *
from admin_module import *
import datetime

# Inicializar el bot
bot = telebot.TeleBot('5674174567:AAEY0jH6SIcKIpt81kv44IFex-6oxyZpFiE')

# Variables
maintenance_mode = False
usuarios_permitidos = [676639963, 1234567890]
usage_count = 1
start_time = time.time()
id_file = 'db/id.json'

# Función para guardar la ID de un usuario
def save_user_id(user_id):
    # Cargar las IDs de usuario existentes
    user_ids = load_user_ids()

    # Si la ID de usuario no está en la lista, agrégala
    if user_id not in user_ids:
        user_ids.append(user_id)

    # Guarda la lista actualizada en el archivo JSON
    with open(id_file, 'w') as file:
        json.dump({"user_ids": user_ids}, file)

# Función para cargar las IDs de usuario desde el archivo
def load_user_ids():
    try:
        with open(id_file, 'r') as file:
            data = json.load(file)
            return data.get('user_ids', [])
    except FileNotFoundError:
        # Si el archivo no existe, retorna una lista vacía
        return []

# Función para verificar si un usuario es administrador (debes implementar esta lógica)
def is_admin(user_id):
    # Aquí puedes implementar la lógica para verificar si un usuario es administrador
    # Esta función debe devolver True si el usuario es administrador, de lo contrario, False
    admin_user_ids = usuarios_permitidos  # Reemplaza con las IDs de los administradores
    return user_id in admin_user_ids

# Función para enviar una notificación a usuarios
def send_notification_to_users(bot, user_ids, message):
    for user_id in user_ids:
        try:
            bot.send_message(user_id, message)
        except Exception as e:
            # Manejar excepciones si falla el envío a un usuario específico
            print(f"No se pudo enviar la notificación a {user_id}: {str(e)}")

# Función para verificar si el modo de mantenimiento está activado
def check_maintenance(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if maintenance_mode and user_id not in usuarios_permitidos:
            bot.reply_to(message, "ℹ️ El bot está en modo de mantenimiento actualmente. ⌛ Por favor, inténtalo más tarde.\n(suena musiquilla de ascensor)")
            return None
        return func(message)
    return wrapped

# Función para incrementar usage_count y manejar el comando
def increment_usage_count(func):
    @wraps(func)
    def wrapped(message):
        global usage_count
        usage_count += 1
        func(message)
    return wrapped

# Función para formatear el tiempo en días, horas, minutos y segundos
def format_time(seconds):
    time_delta = datetime.timedelta(seconds=seconds)
    days, seconds = time_delta.days, time_delta.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} días, {hours} horas, {minutes} minutos y {seconds} segundos"

# Manejar mensajes /opmenu
@bot.message_handler(commands=['opmenu'])
def handle_opmenu(message):
    user_id = message.from_user.id

    if is_admin(user_id):
        options_message = "🛠️ Opciones de Administrador v1.1:\n\n" \
              "/stats - Estadísticas de uso\n" \
              "/mantenimiento - Modo mantenimiento\n" \
              "/notify - Enviar notificación a usuarios\n" \
              "/ads - Administrar anuncios\n"

        bot.reply_to(message, options_message)
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para acceder a las opciones de administrador.")

# Comando para enviar notificaciones a usuarios
@bot.message_handler(commands=['notify'])
def handle_send_notification(message):
    user_id = message.from_user.id

    if is_admin(user_id):
        user_ids = load_user_ids()
        bot.reply_to(message, "Escriba el mensaje que desea enviar a los usuarios:")
        bot.register_next_step_handler(message, notify, user_ids)
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para enviar notificaciones a usuarios.")

# Función para enviar notificaciones
def notify(message, user_ids):
    notification_message = message.text
    send_notification_to_users(bot, user_ids, notification_message)
    bot.reply_to(message, f"Se envió la notificación a {len(user_ids)} usuarios.")

# Manejar mensajes /ads
#@bot.message_handler(commands=['ads'])
#@check_maintenance
#@increment_usage_count
#def handle_np(message):
#    ads_command(bot, message)

# Manejar mensajes /np
@bot.message_handler(commands=['np'])
@check_maintenance
@increment_usage_count
def handle_np(message):
    np_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /dp
@bot.message_handler(commands=['dp'])
@check_maintenance
@increment_usage_count
def handle_dp(message):
    dp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /pl
@bot.message_handler(commands=['pl'])
@check_maintenance
@increment_usage_count
def handle_pl(message):
    pl_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /up
@bot.message_handler(commands=['up'])
@check_maintenance
@increment_usage_count
def handle_up(message):
    up_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /sp
@bot.message_handler(commands=['sp'])
@check_maintenance
@increment_usage_count
def handle_sp(message):
    sp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /pi
@bot.message_handler(commands=['pi'])
@check_maintenance
@increment_usage_count
def handle_pi(message):
    pi_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /mp
@bot.message_handler(commands=['mp'])
@check_maintenance
@increment_usage_count
def handle_mp(message):
    mp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /addapp
@bot.message_handler(commands=['addapp'])
@check_maintenance
@increment_usage_count
def handle_addapp(message):
    addapp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /app
@bot.message_handler(commands=['app'])
@check_maintenance
@increment_usage_count
def handle_app(message):
    app_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /deleteapp
@bot.message_handler(commands=['deleteapp'])
@check_maintenance
@increment_usage_count
def handle_deleteapp(message):
    deleteapp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /editapp
@bot.message_handler(commands=['editapp'])
@check_maintenance
@increment_usage_count
def handle_editapp(message):
    editapp_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /start
@bot.message_handler(commands=['start'])
@check_maintenance
@increment_usage_count
def handle_start(message):
    start_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /list
@bot.message_handler(commands=['list'])
@check_maintenance
@increment_usage_count
def handle_list(message):
    list_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /about
@bot.message_handler(commands=['about'])
@check_maintenance
@increment_usage_count
def handle_about(message):
    about_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /help
@bot.message_handler(commands=['help'])
@check_maintenance
@increment_usage_count
def handle_help(message):
    help_command(bot, message)
    save_user_id(message.from_user.id)
# Manejar mensajes /mantenimiento
@bot.message_handler(commands=['mantenimiento'])
def handle_maintenance(message):
    user_id = message.from_user.id

    if user_id in usuarios_permitidos:
        global maintenance_mode
        maintenance_mode = not maintenance_mode
        if maintenance_mode:
            bot.reply_to(message, "ℹ️ Modo de mantenimiento activado.")
        else:
            bot.reply_to(message, "ℹ️ Modo de mantenimiento desactivado.")
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para activar o desactivar el modo de mantenimiento.")

# Manejar mensajes /stats
@bot.message_handler(commands=['stats'])
@increment_usage_count
def handle_stats(message):
    global start_time
    user_id = message.from_user.id
    current_time = time.time()
    uptime = current_time - start_time

    stats_message = f"📊 Estadísticas del Bot:\n\n" \
                    f"🔄 Veces usado: {usage_count}\n" \
                    f"⏳ Tiempo de actividad: {format_time(uptime)}\n" \
                    f"🛠️ Estado de mantenimiento: {maintenance_mode}\n" \
                    f"✏️ ID de Usuario: {user_id}"

    bot.reply_to(message, stats_message)

# Función para manejar la reconexión
def reconnect():
    while True:
        try:
            # Intentar establecer la conexión
            bot.polling(none_stop=True)
        except Exception as e:
            # Si ocurre un error, esperar un tiempo y volver a intentar
            print("Error de conexión:", e)
            time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente

# Iniciar la reconexión en un hilo separado
reconnect_thread = threading.Thread(target=reconnect)
reconnect_thread.start()