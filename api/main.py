import os
import requests
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder

# Configuración del token del bot de telegram
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '')
application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

# Función de inicio
def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Estoy listo para alertarte sobre precios de criptomonedas.')

application.add_handler(CommandHandler('start', start))

# Función principal llamada por Vercel
def main_handler(event, context):
    return "Bot is running!"

# Inicia la aplicación
application.run_polling()
          
