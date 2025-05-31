import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello World 👋")

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
