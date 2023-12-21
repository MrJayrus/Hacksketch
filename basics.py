import telebot

def help_command(bot, message):
    
    # Responder al mensaje /help
    bot.reply_to(message, f'Los comandos disponibles actualmente son:\n\nℹ️ *INFORMACIÓN*\n/start - Mensaje de inicio\n/help - Muestra éste menú\n/about - Info sobre este bot\n\n📱*APLICACIONES*\n/list - Listar aplicaciones\n/app - Ver detalles de una app\n/addapp - Agrega nueva aplicación\n/editapp - Editar una aplicación\n/deleteapp - Borrar una aplicación\n\n🗂 *PROYECTOS*\n/np - Subir nuevo proyecto\n/pl - Mostrar lista de proyectos\n/up - Actualizar un proyecto\n/dp - Borrar un proyecto\n/sp - Descargar un proyecto\n/pi - Ver información sobre un proyecto\n/mp - Ver mis proyectos\n\nAutor: @MrJayrus \n\n[HACKSKETCH](https://t.me/hacksketch) 2023',parse_mode='Markdown')
    
    # Responder a /start 
def start_command(bot, message):
    # Responder al mensaje /start
    bot.reply_to(message, f'**¡Hola!**\nBienvenido a nuestro bot de gestión de aplicaciones y proyectos. Aquí tendrás acceso a la información más actualizada, podrás descargar, modificar e incluso compartir tus propios proyectos para que otros usuarios los vean y colaboren en ellos.\n\n**¿Qué puedes hacer con nuestro bot?**\n- Ver información actualizada.\n- Descargar proyectos existentes.\n- Modificar tus propios proyectos.\n- Subir nuevos proyectos para compartir con la comunidad.\n\nPara ver una lista completa de opciones disponibles, simplemente escribe el comando: /help\n\n¡Explora todas las funcionalidades y disfruta de una experiencia única con nuestro bot de gestión de aplicaciones y proyectos! Si tienes alguna pregunta, no dudes en consultarnos. ¡Estamos aquí para ayudarte! 🚀',parse_mode='Markdown')
    
def about_command(bot, message):
    # Responder al mensaje /about
    bot.reply_to(message, f'Hacksketch Bot\n\n*Version: 1.5 AdminPower (061123)* \nEste bot esta escrito en Python con el objetivo de gestionar los proyectos, actualmente cuenta con +1000 lineas de código .\n\n*1.5 (06-11-23)*\n- Nuevas características de administración.\n\n*1.4 (30-07-23)*\n- Nueva funcionalidad integrada en fase beta abierta, la cual le permite a los usuarios subir sus proyectos de SketchwarePro sin acabar para que otros lo puedan editar, lo que permite un trabajo en equipo.\n- Nuevos comandos disponibles, puede verlos desde el menú de ayuda usando el comando: /help \n\n*1.4a (30-07-23)*\n- Rediseñado el menú de ayuda.\n\n*1.4b (31-07-23)*\n- Mayor optimización del código.\n\n*1.4c (09-08-23)*\n- Correcciones en los menús y agregado el Panel de control.\n\n*v1.4d (30-08-23)*\n\nSiguenos en: [GitHub](https://github.com/MrJayrus/Hacksketch)\n\n**Con la ayuda de los cursos de Dalto, Python y ChatGPT.**\n\nDesarrollador: @MrJayrus \n\n[HACKSKETCH](https://t.me/+6FTR-rYmerhiYzJh) 2023',parse_mode='Markdown')
