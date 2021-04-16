from .dispatch_handlers import (
    Start,
    Help,
    Echo,
    PlantStatusConversation,
)
from telegram import Bot
from telegram.ext import Dispatcher, Handler
from typing import Optional


class TelegramBot:
    # noinspection PyTypeChecker
    def __init__(self,
                 token: str,
                 base_url: Optional[str] = None):
        self._bot = Bot(token=token, base_url=base_url)
        self._dispatcher = Dispatcher(self._bot, None, workers=0)
        self._dispatcher.add_handler(Start.handler)
        self._dispatcher.add_handler(Help.handler)
        # self._dispatcher.add_handler(Echo.handler)
        self._dispatcher.add_handler(PlantStatusConversation.handler)

    @property
    def bot(self):
        return self._bot

    @property
    def dispatcher(self):
        return self._dispatcher

    def add_handler(self, handler: Handler):
        self._dispatcher.add_handler(handler)
