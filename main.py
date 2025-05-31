from flask import Flask, request
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Your Telegram Bot Token (KEEP THIS SAFE)
BOT_TOKEN = '7949482176:AAGNKwe23jLD6vEfLNn398RCAvFqpLgoRsQ'  # Replace with your real token
bot = telegram.Bot(token=BOT_TOKEN)

# ✅ Your Razorpay payment link and premium group invite
RAZORPAY_LINK = "https://rzp.io/rzp/uZx91zho"  # Replace with your Razorpay link
PREMIUM_LINK = "https://t.me/+XcNakdRjPxVjYjc1"    # Replace with your premium group link

# ================================
# 📩 Telegram Command: /start
# ================================
def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Custom payment link with telegram_id as a note
    payment_link = f"{RAZORPAY_LINK}?notes[telegram_id]={telegram_id}"

    keyboard = [
        [InlineKeyboardButton("💳 Pay & Join Premium", url=payment_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=telegram_id,
        text=f"👋 Hello {name}, click below to pay and get premium access:",
        reply_markup=reply_markup
    )

# ✅ Setup Telegram Bot Updater
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()

# ================================
# 💰 Razorpay Webhook Handler
# ================================
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data.get('event') == 'payment.captured':
        try:
            payment_info = data['payload']['payment']['entity']
            telegram_id = payment_info['notes'].get('telegram_id')

            if telegram_id:
                bot.send_message(
                    chat_id=telegram_id,
                    text=f"✅ Payment received!\nHere is your premium access link:\n{PREMIUM_LINK}"
                )
                return 'Success', 200
            else:
                return '❌ telegram_id missing in Razorpay Notes', 400
        except Exception as e:
            return f"Error: {str(e)}", 500

    return 'Ignored', 200

# ================================
# 🧪 Home Route (for testing)
# ================================
@app.route('/')
def index():
    return "✅ Telegram Bot is Running!"

# ================================
# 🚀 Run Flask App on Render
# ================================
port = int(os.environ.get("PORT", 10000))  # Render assigns a port via env
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
