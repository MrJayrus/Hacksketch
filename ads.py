import telebot
import os
import json
from telebot import types

# Define una lista para almacenar los anuncios
anuncios = []

# Nombre del archivo de anuncios
ads_file = '../db/ads.json'

# Cargar anuncios desde el archivo
def load_ads():
    global anuncios
    try:
        with open(ads_file, 'r') as f:
            anuncios = json.load(f)
    except FileNotFoundError:
        anuncios = []

# Guardar anuncios en el archivo
def save_ads():
    with open(ads_file, 'w') as f:
        json.dump(anuncios, f)

# Comando para mostrar el menú de anuncios (solo para administradores)
def ads_command(bot, message):
    # Verificar si el usuario es administrador
    if is_admin(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("1. Agregar anuncio")
        markup.row("2. Modificar anuncio")
        markup.row("3. Eliminar anuncio")

        bot.reply_to(message, "Menú de Anuncios. V0.1", reply_markup=markup)
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para acceder al menú de anuncios.")

# Comando para agregar un anuncio (opción 1)
@bot.message_handler(func=lambda message: message.text == "1. Agregar anuncio" and is_admin(message.from_user.id))
def handle_add_advertisement(message):
    bot.reply_to(message, "Ingresa el nombre del anuncio:")
    bot.register_next_step_handler(message, get_ad_name)

def get_ad_name(message):
    ad_name = message.text
    bot.reply_to(message, "Ingresa el mensaje del anuncio (formato markdown):")
    bot.register_next_step_handler(message, get_ad_message, ad_name)

def get_ad_message(message, ad_name):
    ad_message = message.text
    bot.reply_to(message, "Ingresa la fecha de expiración del anuncio (formato DD-MM-YYYY):")
    bot.register_next_step_handler(message, get_ad_expiry, ad_name, ad_message)

def get_ad_expiry(message, ad_name, ad_message):
    ad_expiry = message.text
    bot.reply_to(message, "Ingresa cada cuánto tiempo en minutos se enviará el anuncio:")
    bot.register_next_step_handler(message, save_advertisement, ad_name, ad_message, ad_expiry)

def save_advertisement(message, ad_name, ad_message, ad_expiry):
    ad_interval = message.text

    # Validar y guardar el anuncio en la lista
    try:
        ad_interval = int(ad_interval)
        anuncio = {
            'name': ad_name,
            'message': ad_message,
            'expiry': ad_expiry,
            'interval': ad_interval
        }
        anuncios.append(anuncio)

        # Guardar anuncios en el archivo
        save_ads()
        bot.reply_to(message, "Anuncio agregado con éxito.")
    except ValueError:
        bot.reply_to(message, "El intervalo debe ser un número entero en minutos. Por favor, intenta de nuevo.")

# Opción 2: Modificar anuncio
@bot.message_handler(func=lambda message: message.text == "2. Modificar anuncio" and is_admin(message.from_user.id))
def modify_advertisement_option(message):
    bot.reply_to(message, "Estos son los anuncios activos:")
    list_active_ads_for_modification(message)

def list_active_ads_for_modification(message):
    active_ads = [ad['name'] for ad in anuncios]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for ad in active_ads:
        markup.add(ad)
    markup.add("Cancelar")
    bot.reply_to(message, "Selecciona el anuncio que deseas modificar o presiona 'Cancelar':", reply_markup=markup)
    bot.register_next_step_handler(message, select_ad_for_modification)

def select_ad_for_modification(message):
    selected_ad = message.text
    if selected_ad == "Cancelar":
        bot.reply_to(message, "Operación de modificación de anuncio cancelada.")
    else:
        ad = find_advertisement_by_name(selected_ad)
        if ad:
            bot.reply_to(message, f"Detalles del anuncio '{ad['name']}':\n\n{ad['message']}\n\nExpiración: {ad['expiry']}\nIntervalo: {ad['interval']} minutos")
            bot.reply_to(message, "Ingresa el nuevo mensaje del anuncio (formato markdown):")
            bot.register_next_step_handler(message, modify_ad_message, ad)
        else:
            bot.reply_to(message, "El anuncio seleccionado no existe.")

def find_advertisement_by_name(name):
    for ad in anuncios:
        if ad['name'] == name:
            return ad
    return None

def modify_ad_message(message, ad):
    ad_message = message.text
    bot.reply_to(message, "Ingresa la nueva fecha de expiración del anuncio (formato DD-MM-YYYY):")
    bot.register_next_step_handler(message, modify_ad_expiry, ad, ad_message)

def modify_ad_expiry(message, ad, ad_message):
    ad_expiry = message.text
    bot.reply_to(message, "Ingresa el nuevo intervalo de envío del anuncio en minutos:")
    bot.register_next_step_handler(message, save_modified_advertisement, ad, ad_message, ad_expiry)

def save_modified_advertisement(message, ad, ad_message, ad_expiry):
    new_interval = message.text

    # Validar y actualizar los detalles del anuncio
    try:
        new_interval = int(new_interval)
        ad['message'] = ad_message
        ad['expiry'] = ad_expiry
        ad['interval'] = new_interval

        # Guardar anuncios actualizados en el archivo
        save_ads()
        bot.reply_to(message, "Anuncio modificado con éxito.")
    except ValueError:
        bot.reply_to(message, "El intervalo debe ser un número entero en minutos. Por favor, intenta de nuevo.")

# Opción 3: Eliminar anuncio
@bot.message_handler(func=lambda message: message.text == "3. Eliminar anuncio" and is_admin(message.from_user.id))
def delete_advertisement_option(message):
    bot.reply_to(message, "Estos son los anuncios activos:")
    list_active_ads_for_deletion(message)

def list_active_ads_for_deletion(message):
    active_ads = [ad['name'] for ad in anuncios]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for ad in active_ads:
        markup.add(ad)
    markup.add("Cancelar")
    bot.reply_to(message, "Selecciona el anuncio que deseas eliminar o presiona 'Cancelar':", reply_markup=markup)
    bot.register_next_step_handler(message, select_ad_for_deletion)

def select_ad_for_deletion(message):
    selected_ad = message.text
    if selected_ad == "Cancelar":
        bot.reply_to(message, "Operación de eliminación de anuncio cancelada.")
    else:
        ad = find_advertisement_by_name(selected_ad)
        if ad:
            bot.reply_to(message, f"Detalles del anuncio '{ad['name']}':\n\n{ad['message']}\n\nExpiración: {ad['expiry']}\nIntervalo: {ad['interval']} minutos")
            bot.reply_to(message, "¿Estás seguro de que deseas eliminar este anuncio? (si/no)")
            bot.register_next_step_handler(message, confirm_delete_advertisement, ad)
        else:
            bot.reply_to(message, "El anuncio seleccionado no existe.")

def confirm_delete_advertisement(message, ad):
    confirmation = message.text.lower()
    if confirmation == "si":
        # Eliminar el anuncio de la lista de anuncios
        anuncios.remove(ad)
        bot.reply_to(message, "Anuncio eliminado con éxito.")
    elif confirmation == "no":
        bot.reply_to(message, "Eliminación del anuncio cancelada.")
    else:
        bot.reply_to(message, 'Respuesta inválida. Por favor, responde con "si" o "no".')
        
# Define la función para verificar si un usuario es administrador
def is_admin(user_id):
    # Implementa tu lógica para verificar si un usuario es administrador
    return user_id in [123456, 789012]  # Reemplaza con los IDs reales de administradores

# Carga los anuncios al inicio
load_ads()