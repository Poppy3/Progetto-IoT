from ..config import TELEGRAM_API_KEY, TELEGRAM_BASE_URL
from ..telegram_bot import TelegramBot


telegram_bot = TelegramBot(token=TELEGRAM_API_KEY, base_url=TELEGRAM_BASE_URL)
