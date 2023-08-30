import telebot
import os
import time
import threading
from functools import wraps
from app import *
from projects import *
from basics import *
from admin_module import *

# Inicializar el bot
bot = telebot.TeleBot(os.environ['BOT_API'])

# Variables
maintenance_mode = False
usage_count = 1

# Variable para almacenar la cantidad de veces que el bot es usado
usage_count = 0

# Variable para almacenar el tiempo de inicio del bot
start_time = time.time()

# Función para verificar si el modo de mantenimiento está activado
def check_maintenance(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if maintenance_mode and user_id != 1676639963:
            bot.reply_to(message, "ℹ️ El bot está en modo de mantenimiento. ⌛ Por favor, inténtalo más tarde.")
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

# Manejar mensajes /stop
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    user_id = message.from_user.id
    if user_id == 1676639963:  # Cambia este número por tu ID de usuario de Telegram
        bot.reply_to(message, "Apagando bot.")
        # Detener la ejecución del bot
        raise SystemExit
    else:
        bot.reply_to(message, "Acceso denegado!")

# Manejar mensajes /opmenu
@bot.message_handler(commands=['opmenu'])
@check_maintenance
def handle_opmenu(message):
    user_id = message.from_user.id

    if is_admin(user_id):
        options_message = "🛠️ Opciones de Administrador v1.0:\n\n" \
                          "/stats - Estadistísticas de uso\n" \
                          "/mantenimiento - Modo mantenimiento\n" 
        bot.reply_to(message, options_message)
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para acceder a las opciones de administrador.")

# Manejar mensajes /np
@bot.message_handler(commands=['np'])
@check_maintenance
@increment_usage_count
def handle_np(message):
    np_command(bot, message)

# Manejar mensajes /dp
@bot.message_handler(commands=['dp'])
@check_maintenance
@increment_usage_count
def handle_dp(message):
    dp_command(bot, message)

# Manejar mensajes /pl
@bot.message_handler(commands=['pl'])
@check_maintenance
@increment_usage_count
def handle_pl(message):
    pl_command(bot, message)

# Manejar mensajes /up
@bot.message_handler(commands=['up'])
@check_maintenance
@increment_usage_count
def handle_up(message):
    up_command(bot, message)

# Manejar mensajes /sp
@bot.message_handler(commands=['sp'])
@check_maintenance
@increment_usage_count
def handle_sp(message):
    sp_command(bot, message)
    
# Manejar mensajes /pi
@bot.message_handler(commands=['pi'])
@check_maintenance
@increment_usage_count
def handle_pi(message):
    pi_command(bot, message)
    
# Manejar mensajes /mp
@bot.message_handler(commands=['mp'])
@check_maintenance
@increment_usage_count
def handle_mp(message):
    mp_command(bot, message)
    
# Manejar mensajes /addapp
@bot.message_handler(commands=['addapp'])
@check_maintenance
@increment_usage_count
def handle_addapp(message):
    addapp_command(bot, message)

# Manejar mensajes /app
@bot.message_handler(commands=['app'])
@check_maintenance
@increment_usage_count
def handle_app(message):
    app_command(bot, message)

# Manejar mensajes /deleteapp
@bot.message_handler(commands=['deleteapp'])
@check_maintenance
@increment_usage_count
def handle_deleteapp(message):
    deleteapp_command(bot, message)

# Manejar mensajes /editapp
@bot.message_handler(commands=['editapp'])
@check_maintenance
@increment_usage_count
def handle_editapp(message):
    editapp_command(bot, message)

# Manejar mensajes /start
@bot.message_handler(commands=['start'])
@check_maintenance
@increment_usage_count
def handle_start(message):
    start_command(bot, message)

# Manejar mensajes /list
@bot.message_handler(commands=['list'])
@check_maintenance
@increment_usage_count
def handle_list(message):
    list_command(bot, message)

# Manejar mensajes /about
@bot.message_handler(commands=['about'])
@check_maintenance
@increment_usage_count
def handle_about(message):
    about_command(bot, message)

# Manejar mensajes /help
@bot.message_handler(commands=['help'])
@check_maintenance
@increment_usage_count
def handle_help(message):
    help_command(bot, message)

# Manejar mensajes /mantenimiento
@bot.message_handler(commands=['mantenimiento'])
def handle_maintenance(message):
    global maintenance_mode
    user_id = message.from_user.id

    if user_id == 1676639963:  # Cambia este número por tu ID de usuario de Telegram
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
                    f"⏳ Tiempo de actividad: {uptime:.2f} seg\n" \
                    f"🛠 ️Estado de mantenimiento: {maintenance_mode}\n" \
                    f"✏️ ID de Usuario: {user_id}"

    bot.reply_to(message, stats_message)

# Definir updater
updater = Updater(token=os.environ['BOT_API'])

# Iniciar la reconexión en un hilo separado
def reconnect():
    while True:
        try:
            # Intentar establecer la conexión
            updater.start_polling()
        except Exception as e:
            # Si ocurre un error, esperar un tiempo y volver a intentar
            print("Error de conexión:", e)
            time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente
reconnect()
