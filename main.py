from flask import Flask, request
import telegram
import requests
import os

app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = '7949482176:AAGNKwe23jLD6vEfLNn398RCAvFqpLgoRsQ' 
bot = telegram.Bot(token=BOT_TOKEN)

# Razorpay API credentials
RAZORPAY_LINK = "https://rzp.io/rzp/uZx91zho"  # Replace with your Razorpay link
PREMIUM_LINK = "https://t.me/+XcNakdRjPxVjYjc1"    # Replace with your premium group link

# Premium Telegram group link
PREMIUM_LINK = "https://t.me/+YOURGROUPINVITELINK"

@app.route('/')
def home():
    return "Bot is running!"

# Telegram command handler
@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    message = data['message']
    chat_id = message['chat']['id']

    # Create Razorpay payment link
    link_data = {
        "amount": 10000,  # ₹100.00 (in paise)
        "currency": "INR",
        "accept_partial": False,
        "description": "Access to Premium Telegram Group",
        "customer": {
            "name": str(chat_id),
            "email": "test@example.com"  # dummy; Razorpay needs one
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
        "https://api.razorpay.com/v1/payment_links",
        auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
        json=link_data
    )
    
    payment_link = response.json()['short_url']

    bot.send_message(
        chat_id=chat_id,
        text=f"💳 Please complete the payment to access the premium group:\n{payment_link}"
    )

    return '', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'payment.captured':
        payment_info = data['payload']['payment']['entity']
        telegram_id = payment_info['notes'].get('telegram_id')

        if telegram_id:
            bot.send_message(
                chat_id=telegram_id,
                text=f"✅ Payment received! Here is your premium access:\n{PREMIUM_LINK}"
            )
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
from flask import Flask, request
import telegram
import requests
import os

app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telegram.Bot(token=BOT_TOKEN)

# Razorpay API credentials
RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_key_secret'

# Premium Telegram group link
PREMIUM_LINK = "https://t.me/+YOURGROUPINVITELINK"

@app.route('/')
def home():
    return "Bot is running!"

# Telegram command handler
@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    message = data['message']
    chat_id = message['chat']['id']

    # Create Razorpay payment link
    link_data = {
        "amount": 10000,  # ₹100.00 (in paise)
        "currency": "INR",
        "accept_partial": False,
        "description": "Access to Premium Telegram Group",
        "customer": {
            "name": str(chat_id),
            "email": "test@example.com"  # dummy; Razorpay needs one
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
        "https://api.razorpay.com/v1/payment_links",
        auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
        json=link_data
    )
    
    payment_link = response.json()['short_url']

    bot.send_message(
        chat_id=chat_id,
        text=f"💳 Please complete the payment to access the premium group:\n{payment_link}"
    )

    return '', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'payment.captured':
        payment_info = data['payload']['payment']['entity']
        telegram_id = payment_info['notes'].get('telegram_id')

        if telegram_id:
            bot.send_message(
                chat_id=telegram_id,
                text=f"✅ Payment received! Here is your premium access:\n{PREMIUM_LINK}"
            )
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
