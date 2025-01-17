import os
import requests
from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder

app = Flask(__name__)

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', '')

application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

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

def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Estoy listo para alertarte sobre precios de criptomonedas. Usa /alert nombreactivo valor para configurar una alerta.')

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('alert', alert))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
