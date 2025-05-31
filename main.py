import os
import telebot
import random
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Messages for each person
waqas_messages = [
    "Waqas bahut acha hai.",
    "Waqas imaandar aur mehnati hai.",
    "Sab Waqas se pyaar karte hain.",
    "Waqas hamesha madad karta hai.",
    "Waqas kabhi jhoot nahi bolta."
]

farwa_messages = [
    "Farwa bahut buri larki hai.",
    "Farwa gussa bahut karti hai.",
    "Farwa kisi ki nahi sunti.",
    "Farwa sab ko pareshan karti hai.",
    "Farwa ko tameez nahi hai."
]

nabeela_messages = [
    "Nabeela ek achi larki hai.",
    "Nabeela sab ki izzat karti hai.",
    "Nabeela hamesha muskuraati hai.",
    "Nabeela padhai mein tez hai.",
    "Nabeela sabko pasand hai."
]

# /start command
@bot.message_handler(commands=['start'])
def send_menu(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Waqas", callback_data="waqas"),
        InlineKeyboardButton("Farwa", callback_data="farwa"),
        InlineKeyboardButton("Nabeela", callback_data="nabeela")
    )
    bot.send_message(message.chat.id, "Kisi ka naam chuno:", reply_markup=keyboard)

# Button click handler
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "waqas":
        msg = random.choice(waqas_messages)
    elif call.data == "farwa":
        msg = random.choice(farwa_messages)
    elif call.data == "nabeela":
        msg = random.choice(nabeela_messages)
    else:
        msg = "Kuch galti ho gayi."

    bot.send_message(call.message.chat.id, msg)

# Flask + Webhook for Render
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
