from ..extensions.teleflask import bot
from flask import Blueprint
from teleflask.messages import HTMLMessage


telegram_bot_bp = Blueprint('telegram_bot', __name__, url_prefix='/bot')


@bot.on_command('test')
def test(update, text):
    # update is the update object. It is of type pytgbot.api_types.receivable.updates.Update
    # text is the text after the command. Can be empty. Type is str.
    return HTMLMessage("<b>Hello!</b> Thanks for using my bot!")
    # return TextMessage("<b>Hello!</b> Thanks for using my bot!", parse_mode="html")
