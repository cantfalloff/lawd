import os

from dotenv import load_dotenv


load_dotenv(override=True)

telegram_bot_token = os.getenv('telegram_bot_token')
