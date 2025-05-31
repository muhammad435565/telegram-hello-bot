import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Start command
@bot.message_handler(commands=['start'])
def send_menu(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Waqas", callback_data="waqas"),
        InlineKeyboardButton("Farwa", callback_data="farwa"),
        InlineKeyboardButton("Nabeela", callback_data="nabeela")
    )
    bot.send_message(message.chat.id, "Kisi ek ka naam chuno:", reply_markup=keyboard)

# Jab koi button click kare
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "waqas":
        msg = (
            "Waqas ek acha insaan hai.\n"
            "Woh sab ki madad karta hai.\n"
            "Kabhi jhoot nahi bolta.\n"
            "Mehnati hai aur imaandar hai.\n"
            "Sab usse pyaar karte hain."
        )
    elif call.data == "farwa":
        msg = (
            "Farwa bilkul pasand nahi.\n"
            "Woh gussa karti hai.\n"
            "Baat nahi sunti.\n"
            "Sab ko pareshaan karti hai.\n"
            "Bahut gandi harkatein karti hai."
        )
    elif call.data == "nabeela":
        msg = (
            "Nabeela ek bahut achi larki hai.\n"
            "Hamesha muskuraati rehti hai.\n"
            "Sab ki izzat karti hai.\n"
            "Parhai me tez hai.\n"
            "Use sab pasand karte hain."
        )
    else:
        msg = "Kuch galat ho gaya."

    bot.send_message(call.message.chat.id, msg)

# Webhook setup
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
