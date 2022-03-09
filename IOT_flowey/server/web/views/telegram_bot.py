from ..extensions.telegram_bot import telegram_bot
from flask import Blueprint, request, Response
from telegram import Update


telegram_bot_bp = Blueprint('telegram_bot', __name__, url_prefix='/telegram_bot')


@telegram_bot_bp.route('/get_webhook_info')
def get_webhook_info_response():
    info = telegram_bot.bot.get_webhook_info().to_json()
    return Response(info, status=200, content_type='application/json')


@telegram_bot_bp.route('/set_webhook')
def set_webhook():
    print(f'{request.url_root[:-1]}{telegram_bot_bp.url_prefix}/{telegram_bot.bot.token}')
    success = telegram_bot.set_webhook(webhook_url=f'{request.url_root[:-1]}{telegram_bot_bp.url_prefix}'
                                                   f'/{telegram_bot.bot.token}')
    if success:
        return get_webhook_info_response()
    else:
        return Response('Webhook not set', status=500)


@telegram_bot_bp.route('/delete_webhook')
def delete_webhook():
    telegram_bot.bot.delete_webhook()
    return get_webhook_info_response()


@telegram_bot_bp.route(f'/{telegram_bot.bot.token}', methods=['POST'])
def webhook():
    # retrieve the message in JSON and then transform it to Telegram object
    payload = request.get_json(force=True)
    print(f'Webhook Payload = {payload}')
    try:
        update = Update.de_json(payload, telegram_bot.bot)
        telegram_bot.dispatcher.process_update(update)

    except Exception as e:
        print('ERROR - views/telegram_bot.py .webhook()')
        print(e)
    return ''
