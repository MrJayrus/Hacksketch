# Función para verificar si el usuario es un administrador
def is_admin(user_id):

    return user_id == 1676639963  # Ejemplo: Cambia este número por tu ID de usuario de Telegram

# Función para eliminar un proyecto de la base de datos
def delete_project(bot, message):
    if is_admin(message.from_user.id):
        # Agrega aquí la lógica para eliminar un proyecto de la base de datos
        bot.reply_to(message, "🗑️ Enviar el nombre del proyecto que deseas eliminar, o 'Cancelar' para cancelar.")
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para eliminar proyectos de la base de datos.")

# Función para limpiar la base de datos de proyectos
def clear_projects_db(bot, message):
    if is_admin(message.from_user.id):
        # Agrega aquí la lógica para limpiar la base de datos de proyectos
        bot.reply_to(message, "⚠️ Advertencia: Esta acción borrará todos los proyectos. Para confirmar, responde con 'BORRAR'.")
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para limpiar la base de datos de proyectos.")