# bot.py
import telebot
from shortener import shorten_url
import validators
import sqlite3
from datetime import datetime
import pytz  # For timezone handling
import os
API_TOKEN = os.getenv('TGBToken')
bot = telebot.TeleBot(API_TOKEN)
# Update this to your actual server URL if hosted elsewhere

def get_current_ist():
    return datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

def get_time_based_greeting():
    # Define timezone for IST
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    
    # Get the current hour in IST
    current_hour = now.hour
    
    # Determine the part of the day
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 21:
        return "Good evening"
    else:
        return "Good night"



@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO telegram_users (user_id, username, full_name) VALUES (?, ?, ?)',
              (message.from_user.id, message.from_user.username, message.from_user.full_name))
    conn.commit()
    conn.close()
    user = message.from_user
    user_name = user.username if user.username else user.first_name
    
    # Get the time-based greeting
    greeting = get_time_based_greeting()
    
    # Get the current IST time
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create inline keyboard
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("\U0001F5BC Instagram", url="https://www.instagram.com/kannadagamershub"),
        telebot.types.InlineKeyboardButton("🌐 Website", url="https://kannadagamershub.000webhostapp.com")
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton("\U0001F3A5 YouTube Channel", url="https://www.youtube.com/@KannadaGamershub"),
        telebot.types.InlineKeyboardButton("\U0001F4F1 WhatsApp Channel", url="https://whatsapp.com/channel/0029VaU05uG9RZAeiXKyEu06")
    )
    
    # Send message with inline keyboard
    bot.reply_to(message, f"{greeting}, {user_name}!\nThe current IST time is {current_time}.\nSend Url To Be Shorten:.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    original_url = message.text
    if validators.url(original_url):
        short_code = shorten_url(original_url)
        short_url = f"{os.getenv('Url')}/{short_code}"
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('UPDATE telegram_users SET links_shortened = links_shortened + 1, last_visited = ? WHERE user_id = ?',
                  (get_current_ist(), message.from_user.id))
        conn.commit()
        conn.close()
        
        bot.reply_to(message, f'Shortened URL: {short_url}\nThankyou')
    else:
        bot.reply_to(message, "Invalid URL. Please send a valid URL to shorten.")

def start_bot():
    bot.polling()

if __name__ == '__main__':
    start_bot()

