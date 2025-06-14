from flask import Flask, request
import telegram
import requests
import json

# --- CONFIGURATION ---

# Telegram Bot Token
BOT_TOKEN = '7949482176:AAGNKwe23jLD6vEfLNn398RCAvFqpLgoRsQ'
bot = telegram.Bot(token=BOT_TOKEN)

# Razorpay Test Keys
RAZORPAY_KEY_ID = 'rzp_test_8XvL45O5H6KfyC'
RAZORPAY_KEY_SECRET = 'F9jwbf7xYSF7fuiwfFFi2uQE'

# Premium Telegram Group Invite Link
PREMIUM_GROUP_LINK = "https://t.me/+R5HLRsfd7K0wNjVl"

# Flask App
app = Flask(__name__)

# --- ROUTES ---

@app.route('/')
def home():
    return "✅ Telegram + Razorpay Bot is Live!"

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    print("📩 Telegram Webhook:", json.dumps(data, indent=2))

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message'].get('text', '')

        if message_text == '/start':
            bot.send_message(chat_id=chat_id, text="👋 Welcome! Creating your payment link...")
            create_payment_link(chat_id)
    return '', 200

def create_payment_link(chat_id):
    url = "https://api.razorpay.com/v1/payment_links"

    link_data = {
        "amount": 2000,  # ₹20.00 in paise
        "currency": "INR",
        "accept_partial": False,
        "description": "Access to Premium Telegram Group",
        "customer": {
            "name": str(chat_id),
            "email": "test@example.com",
            "contact": "9876543210"  # ✅ Use realistic number
        },
        "notify": {"sms": False, "email": False},
        "reminder_enable": False,
        "notes": {
            "telegram_id": str(chat_id)
        },
        "callback_url": "https://tel-ntvy.onrender.com/webhook"
    }

    try:
        response = requests.post(
            url,
            auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
            data=json.dumps(link_data),
            headers={'Content-Type': 'application/json'}
        )

        result = response.json()
        print("🔍 Razorpay API Response:")
        print(json.dumps(result, indent=2))

        if 'short_url' in result:
            payment_url = result['short_url']
            bot.send_message(chat_id=chat_id, text=f"💳 Click below to pay ₹20 and get premium access:\n{payment_url}")
        else:
            error_message = result.get("error", {}).get("description", "Unknown Razorpay error.")
            bot.send_message(chat_id=chat_id, text=f"❌ Payment link could not be created:\n{error_message}")

    except Exception as e:
        print("❌ Exception while creating Razorpay link:", str(e))
        bot.send_message(chat_id=chat_id, text="❌ An error occurred while creating the payment link.")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Razorpay Webhook Received:")
    print(json.dumps(data, indent=2))

    if data.get('event') == 'payment.captured':
        payment_info = data['payload']['payment']['entity']
        telegram_id = payment_info['notes'].get('telegram_id')

        if telegram_id:
            try:
                bot.send_message(
                    chat_id=int(telegram_id),
                    text=f"✅ Payment received! 🎉\nHere is your premium group access:\n{PREMIUM_GROUP_LINK}"
                )
            except Exception as e:
                print(f"❌ Error sending message to Telegram user {telegram_id}: {e}")
    return '', 200

# --- RUN APP ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
