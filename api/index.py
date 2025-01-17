import os
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder

# Reemplaza 'YOUR TELEGRAM TOKEN HERE' con tu token
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '')
application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

# Diccionario para almacenar las alertas
alerts = {}

def get_crypto_price(symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data[symbol]['usd']  # Devuelve el precio en USD

def alert(update: Update, context: CallbackContext):
    try:
        if len(context.args) != 2:
            update.message.reply_text('Error: Usa el formato /alert nombreactivo valor.')
            return

        crypto, value = context.args
        value = float(value)
        chat_id = update.effective_chat.id

        if chat_id not in alerts:
            alerts[chat_id] = []

        alerts[chat_id].append((crypto, value))

        update.message.reply_text(f'Alerta configurada para {crypto} a {value} USD')
    
    except ValueError:
        update.message.reply_text('Error: Asegúrate de ingresar un número válido para el valor.')

def check_alerts(context: CallbackContext):
    for chat_id in alerts:
        for crypto, value in alerts[chat_id][:]:
            current_price = get_crypto_price(crypto)
            if current_price >= value:
                context.bot.send_message(chat_id=chat_id, text=f'¡Alerta! {crypto} alcanzó los {value} USD.')
                alerts[chat_id].remove((crypto, value))

# Añade la función start y el manejador del comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Estoy listo para alertarte sobre precios de criptomonedas. Usa /alert nombreactivo valor para configurar una alerta.')

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('alert', alert))

# Esta función será llamada por Vercel
def main_handler(event, context):
    # Maneja la lógica de webhook aquí
    return "Bot is running!"

# Llama a la función check_alerts cada 60 segundos
import time
import threading

def run_check_alerts():
    while True:
        check_alerts(None)
        time.sleep(60)

threading.Thread(target=run_check_alerts).start()

# Inicia la aplicación
application.run_polling()
