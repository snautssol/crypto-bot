import os
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder

# Reemplaza 'YOUR TELEGRAM TOKEN HERE' con tu token
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '')
application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Estoy listo para alertarte sobre precios de criptomonedas. Usa /alert nombreactivo valor para configurar una alerta.')

application.add_handler(CommandHandler('start', start))

def main_handler(event, context):
    return "Bot is running!"

# Inicia la aplicación
application.run_polling()
