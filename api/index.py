import os
import requests
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder

app = Flask(__name__)

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '')

# Configuración del bot de Telegram
application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

alerts = {}

def get_crypto_price(symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data[symbol]['usd']  # Devuelve el precio en USD

# Handlers de comandos
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

def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Estoy listo para alertarte sobre precios de criptomonedas. Usa /alert nombreactivo valor para configurar una alerta.')

# Agregar handlers al bot
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('alert', alert))

@app.route('/')
def home():
    return jsonify({"message": "¡Hola! Esta es la API de tu bot de Telegram."})

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    # Configura el webhook de Telegram
    app_url = os.getenv('APP_URL')  # Asegúrate de configurar esta variable en Vercel
    if TELEGRAM_API_TOKEN and app_url:
        application.bot.set_webhook(url=f"{app_url}/webhook")
    
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
            
