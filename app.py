
import os
import telebot
from flask import Flask, render_template
import threading

# Récupère le Token depuis les réglages de Render
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- PARTIE WEB ---
@app.route('/')
def index():
    return render_template('index.html')

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- PARTIE BOT TELEGRAM ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Remplace l'URL ci-dessous par celle de TON service Render une fois qu'il sera créé
    web_app_url = "https://fifa-bot-web.onrender.com"
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_button = telebot.types.InlineKeyboardButton(
        text="🎮 Ouvrir la PLATEFORME FIFA 🎮", 
        web_app=telebot.types.WebAppInfo(url=web_app_url)
    )
    keyboard.add(web_app_button)
    
    bot.send_message(message.chat.id, "Bienvenue sur le Predictor FIFA ! Cliquez ci-dessous pour accéder à la plateforme.", reply_markup=keyboard)

def run_bot():
    bot.infinity_polling()

# --- LANCEMENT ---
if __name__ == '__main__':
    # Lancement en parallèle
    threading.Thread(target=run_flask).start()
    run_bot()
