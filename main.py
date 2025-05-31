from flask import Flask, request
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

app = Flask(__name__)

# Your bot token from BotFather
BOT_TOKEN = '7949482176:AAGNKwe23jLD6vEfLNn398RCAvFqpLgoRsQ'
bot = telegram.Bot(token=BOT_TOKEN)

# Your Razorpay base link
RAZORPAY_LINK = "https://rzp.io/rzp/uZx91zho"  # replace with your real one
# Your premium group invite link
PREMIUM_LINK = "https://t.me/+XcNakdRjPxVjYjc1"

# ---------------------------- BOT HANDLER ----------------------------

def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.id
    name = update.effective_user.first_name

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

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()

# ---------------------------- WEBHOOK ----------------------------

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'payment.captured':
        try:
            entity = data['payload']['payment']['entity']
            telegram_id = entity['notes'].get('telegram_id')
            if telegram_id:
                bot.send_message(chat_id=telegram_id, text=f"✅ Payment received!\nHere is your premium access:\n{PREMIUM_LINK}")
                return 'Sent', 200
            else:
                return '❌ telegram_id missing', 400
        except Exception as e:
            return f"Error: {str(e)}", 500
    return 'Ignored', 200

@app.route('/')
def index():
    return "Bot is running!"
