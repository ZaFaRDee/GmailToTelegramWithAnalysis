# config.py

from dotenv import load_dotenv
import os

load_dotenv()  # .env faylni yuklaydi

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_FOLDER = os.getenv('GMAIL_FOLDER', 'INBOX')  # default: INBOX

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
