import telebot
import json
import os

# Archivo JSON para almacenar la información de los proyectos
proyectos_file = '../db/reportes.json'
apps_db = '../db/apps.json'
proj_db = '../db/proyectos.json'

# Crear el bot
bot = telebot.TeleBot('5674174567:AAGJjOZod9ElDh6dTZHYYThKWqUQbu7H-WM')

# Manejar el comando /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "¡Hola! Soy un bot para reportar errores. Usa el comando /reporte para comenzar.")

# Manejar el comando /reporte
@bot.message_handler(commands=['reporte'])
def report_command(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Aplicación', 'Proyecto')
    bot.reply_to(message, "¿A qué desea reportar el error?", reply_markup=markup)
    bot.register_next_step_handler(message, get_report_type)

def get_report_type(message):
    type = message.text.lower()

    if type == 'aplicación' or type == 'aplicacion' or type == '1' or type == 'app':
        type = apps_db
    elif type == 'proyecto' or type == '2':
        type = proj_db
    else:
        bot.reply_to(message, "Opción no válida. Por favor, elige entre 'Aplicación' o 'Proyecto'.")
        return

    bot.reply_to(message, "Por favor envíame el nombre de la app/proyecto que tiene error:")
    bot.register_next_step_handler(message, lambda m: get_pid(m, type))

def get_pid(message, type):
    name = message.text.lower()
    with open(type, 'r') as f:
        data = json.load(f)
        if name in data:
            pid = data[name]['pid']
            bot.reply_to(message, "Por favor escriba el informe de error en no más de 500 caracteres (letras, números o puntos y comas):")
            bot.register_next_step_handler(message, lambda m: save_report(m, pid))
        else:
            bot.reply_to(message, "No se encontró la app/proyecto con ese nombre.")

def save_report(message, pid):
    report = message.text[:500]
    with open(proyectos_file, 'r') as f:
        data = json.load(f)
    data[pid] = report
    with open(proyectos_file, 'w') as f:
        json.dump(data, f)
    bot.reply_to(message, "El informe ha sido guardado con éxito.")

# Iniciar el bot
bot.polling()
