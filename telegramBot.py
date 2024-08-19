import os
import requests
import telebot

from dotenv import load_dotenv

import logging

telebot.logger.setLevel(logging.WARNING)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def start_bot():
    bot.infinity_polling()


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        f"Hi there, It`s Libary Service. \nNice to see you {message.from_user.first_name} {message.from_user.last_name} \nYour id is {message.from_user.id}",
    )


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        return None
    return response.json()
