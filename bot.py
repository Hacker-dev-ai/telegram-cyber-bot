import telebot
from telebot import types
import os
import json

# Set your API token here
API_TOKEN = "7520128825:AAF_USSJGwqBHOrtRPlaoQtwvG6BxZzjeII"

# Initialize bot
bot = telebot.TeleBot(API_TOKEN)

# JSON file to store paid users
DB_FILE = "users.json"

def load_users():
    """Load user data from JSON file."""
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save user data to JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Load paid users from file
paid_users = load_users()

# Course links
FREE_COURSE_LINK = "https://youtu.be/HrqYGTK8-bo?si=UvWtYXTgDLy9-Apb"
PAID_COURSE_LINK = "https://youtu.be/FNiBNdM7srE?si=aBdpUKLvxhOcBJZ0"

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    free_btn = types.KeyboardButton("📚 Free Course")
    paid_btn = types.KeyboardButton("💰 Paid Course")
    help_btn = types.KeyboardButton("❓ Help")
    markup.add(free_btn, paid_btn, help_btn)

    bot.send_message(message.chat.id, "👋 Welcome! Choose an option:", reply_markup=markup)

# Handle messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.chat.id)

    if message.text == "📚 Free Course":
        bot.send_message(message.chat.id, f"Here is the free course: {FREE_COURSE_LINK}")

    elif message.text == "💰 Paid Course":
        if user_id in paid_users:
            bot.send_message(message.chat.id, f"✅ You have access!\nPaid Course: {PAID_COURSE_LINK}")
        else:
            bot.send_message(message.chat.id, "❌ You haven't purchased access yet.\nComplete payment at https://example.com/payment\nThen send /verify <transaction_id>.")

    elif message.text == "❓ Help":
        bot.send_message(message.chat.id, "Need help? Contact @YourSupportUsername.")

    else:
        bot.send_message(message.chat.id, "❌ Invalid option. Use the menu.")

# Verify payment
@bot.message_handler(commands=['verify'])
def verify(message):
    user_id = str(message.chat.id)
    transaction_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not transaction_id:
        bot.send_message(message.chat.id, "⚠️ Usage: /verify <transaction_id>")
        return

    # Fake transaction verification (Replace with real API)
    if transaction_id.startswith("TXN"):
        paid_users[user_id] = True
        save_users(paid_users)
        bot.send_message(message.chat.id, "✅ Payment verified! You now have access to the paid course.")
    else:
        bot.send_message(message.chat.id, "❌ Invalid transaction ID.")

# Run the bot
if __name__ == '__main__':
    bot.polling()
