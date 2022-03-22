from telegram import Bot

import config as cfg


bot = Bot(token=cfg.TELEGRAM_BOT.API_KEY)


def send_admin_message(text, chat_id=cfg.TELEGRAM_BOT.ADMIN_CHAT_ID):
    bot.send_message(chat_id=chat_id, text=text)
