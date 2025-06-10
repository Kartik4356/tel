from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
import requests
import json
import os

# --- CONFIGURATION ---

# Your Telegram Bot Token
BOT_TOKEN = '7949482176:AAGNKwe23jLD6vEfLNn398RCAvFqpLgoRsQ'
bot = telegram.Bot(token=BOT_TOKEN)

# Razorpay Test Keys
RAZORPAY_KEY_ID = 'rzp_test_8XvL45O5H6KfyC'
RAZORPAY_KEY_SECRET = 'F9jwbf7xYSF7fuiwfFFi2uQE'

# Telegram Premium Group Invite Link
PREMIUM_GROUP_LINK = "https://t.me/+2S_UBsFqIXsyMDU1"

# Flask App
app = Flask(__name__)

# --- TELEGRAM COMMAND HANDLER ---

def start(update, context):
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name
    message = f"Hi {name}! 👋\nClick the link below to pay ₹20 and join the premium group:"
    pay_url = f"https://tel-ntvy.onrender.com/create_payment/{chat_id}"
    bot.send_message(chat_id=chat_id, text=message + "\n" + pay_url)

# --- TELEGRAM WEBHOOK ROUTE ---

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# --- PAYMENT LINK CREATION ---

@app.route('/create_payment/<int:chat_id>')
def create_payment(chat_id):
    url = "https://api.razorpay.com/v1/payment_links"

    link_data = {
        "amount": 2000,  # ₹20 in paise
        "currency": "INR",
        "accept_partial": False,
        "description": "Access to Premium Telegram Group",
        "customer": {
            "name": str(chat_id),
            "email": "test@example.com"
        },
        "notify": {"sms": False, "email": False},
        "reminder_enable": False,
        "notes": {
            "telegram_id": str(chat_id)
        },
        "callback_url": "https://tel-ntvy.onrender.com/webhook",
        "callback_method": "post"
    }

    response = requests.post(
        url,
        auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
        data=json.dumps(link_data),
        headers={'Content-Type': 'application/json'}
    )

    result = response.json()
    payment_url = result['short_url']
    bot.send_message(chat_id=chat_id, text=f"Click below to pay ₹20 and get premium access:\n{payment_url}")
    return "Payment link sent to Telegram!"

# --- RAZORPAY WEBHOOK ---

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'payment.captured':
        payment_info = data['payload']['payment']['entity']
        telegram_id = payment_info['notes'].get('telegram_id')
        if telegram_id:
            bot.send_message(chat_id=telegram_id, text=f"✅ Payment received! Here's your premium access:\n{PREMIUM_GROUP_LINK}")
    return '', 200

# --- DISPATCHER SETUP ---

from telegram.ext import Dispatcher

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))

# --- HOME PAGE ---

@app.route('/')
def home():
    return "Telegram + Razorpay bot is live!"

# --- RUN FLASK APP ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
