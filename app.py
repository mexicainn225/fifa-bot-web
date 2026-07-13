import os
import database  # On importe le fichier qu'on vient de créer
from flask import Flask, render_template
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
# Remplace par ton ID admin (la suite de chiffres)
TON_ID_ADMIN = 5724620019 

@app.route('/')
def home():
    return render_template('index.html')

async def start(update, context):
    user_id = update.effective_user.id
    
    # Vérifie si l'utilisateur est déjà validé dans database.py
    if database.est_valide(user_id):
        keyboard = [[InlineKeyboardButton("🎮 Lancer la PLATEFORME FIFA", web_app=WebAppInfo(url="https://fifa-bot-web.onrender.com"))]]
        await update.message.reply_text("Bienvenue de nouveau ! Voici ton accès :", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Bienvenue ! Pour accéder aux prédictions, envoie ton ID de compte FIFA.")

async def handle_message(update, context):
    user_id = update.effective_user.id
    id_fifa = update.message.text
    
    # Enregistre l'ID reçu dans la base de données
    database.ajouter_utilisateur(user_id, id_fifa)
    
    await update.message.reply_text("ID reçu ! J'attends la validation de l'admin.")
    
    # Envoie une alerte à toi (admin) pour valider
    await context.bot.send_message(TON_ID_ADMIN, f"🚨 Validation requise pour {user_id}. ID: {id_fifa}\n\nCommande pour valider : /valider {user_id}")

async def valider(update, context):
    # Sécurité : seul toi peux utiliser cette commande
    if update.effective_user.id != TON_ID_ADMIN:
        return
    
    if context.args:
        uid = int(context.args[0])
        database.valider_utilisateur(uid)
        keyboard = [[InlineKeyboardButton("🎮 Lancer la PLATEFORME", web_app=WebAppInfo(url="https://fifa-bot-web.onrender.com"))]]
        await context.bot.send_message(uid, "✅ Validé ! Accès débloqué.", reply_markup=InlineKeyboardMarkup(keyboard))
        await update.message.reply_text(f"Utilisateur {uid} validé avec succès !")

if __name__ == '__main__':
    # Lance le serveur web en arrière-plan
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    
    # Lance le bot Telegram
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("valider", valider))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.run_polling()
