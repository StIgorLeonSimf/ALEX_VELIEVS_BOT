import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PAYMENTS_TOKEN = os.getenv('BOT_PAYMENTS_TOKEN')

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not PAYMENTS_TOKEN:
    raise ValueError("BOT_PAYMENTS_TOKEN не найден в .env файле!")


