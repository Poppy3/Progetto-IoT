from .utils import get_keyboard_layout, escape_markdown_V2, get_plant_data_report
from .filters import FilterOnModelColumn
from ..models.plant_data import PlantDataModel
from ..models.plant_type import PlantTypeModel
from abc import ABC, abstractmethod
from itertools import chain
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    BaseFilter,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    Handler,
    MessageHandler,
)

import re


class AbstractHandler(ABC):
    @property
    @abstractmethod
    def handler(self) -> Handler:
        pass


class AbstractCommandHandler(AbstractHandler, ABC):
    @property
    @abstractmethod
    def _command(self) -> str:
        return ''

    @staticmethod
    @abstractmethod
    def _callback(update: Update, ctx: CallbackContext) -> None:
        pass

    @property
    def handler(self) -> Handler:
        return CommandHandler(self._command, self._callback)


class AbstractMessageHandler(AbstractHandler, ABC):
    @property
    @abstractmethod
    def _filters(self) -> BaseFilter:
        pass

    @staticmethod
    @abstractmethod
    def _callback(update: Update, ctx: CallbackContext) -> None:
        pass

    @property
    def handler(self) -> Handler:
        return MessageHandler(self._filters, self._callback)


class StartCLS(AbstractCommandHandler):
    @property
    def _command(self) -> str:
        return 'start'

    @staticmethod
    def _callback(update: Update, _: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        update.message.reply_markdown_v2(
            f'Hi {user.mention_markdown_v2()}\!\n'
            f'My name is Flowey Bot\. Use /help to know what i can do for you\.'
        )


class HelpCLS(AbstractCommandHandler):
    @property
    def _command(self) -> str:
        return 'help'

    @staticmethod
    def _callback(update: Update, _: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text(
            'Here\'s a list of commands I can understand:\n'
            ' · /start - Displays a welcome message\n'
            ' · /help - Displays this message\n'
            ' · /plant_status - I\'ll help you know the status of your plants!\n'
            ' · ... more soon! ...'
        )


class EchoCLS(AbstractMessageHandler):
    @property
    def _filters(self) -> BaseFilter:
        return Filters.text & ~Filters.command

    @staticmethod
    def _callback(update: Update, _: CallbackContext) -> None:
        """Echo the user message."""
        update.message.reply_text(update.message.text)


class PlantStatusCLS(AbstractHandler):

    REGEX = r'^(?P<name>\w+)\s*\((?P<gateway>\w+)\)$'

    class States:
        BRIDGE_SELECTED = 0
        PLANT_SELECTED = 1
        END = ConversationHandler.END

    class Callbacks:
        @staticmethod
        def start(update: Update, _: CallbackContext) -> int:
            """Send a message when the command /status is issued.
            Start step of a multi-step conversation"""
            query_results = (PlantDataModel.query
                             .with_entities(PlantDataModel.bridge_id)
                             .distinct()
                             .order_by(PlantDataModel.bridge_id)
                             .all())
            reply_keyboard = get_keyboard_layout(list(chain(*query_results)))

            update.message.reply_markdown_v2('Please select the group of plants you want to check the status of\.\n\n'
                                             'Reply /cancel in any moment to end this conversation\.',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PlantStatusCLS.States.BRIDGE_SELECTED

        @staticmethod
        def bridge_selected(update: Update, ctx: CallbackContext) -> int:
            # continuation of Conversation started with '/status' command
            bridge_selected = update.message.text
            ctx.user_data['bridge_selected'] = bridge_selected
            query_results = (PlantDataModel.query
                             .join(PlantTypeModel)
                             .with_entities(PlantDataModel.gateway_id, PlantTypeModel.name)
                             .filter(PlantDataModel.bridge_id == bridge_selected)
                             .order_by(PlantTypeModel.name)
                             .distinct()
                             .all())
            keys = [f'{name} ({gtw_id})' for (gtw_id, name) in query_results]
            reply_keyboard = get_keyboard_layout(keys)

            # TODO prendi le piante dal model, e stampa un report sommario
            update.message.reply_markdown_v2(
                f'You selected the group "{escape_markdown_V2(bridge_selected)}"\.\n\n'
                # f'<Qui mostro il report sommario delle piante del bridge selezionato\>\n\n'
                f'Please select the plant you want to check the status of, '
                f'or reply with /cancel to end the conversation\.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )
            return PlantStatusCLS.States.PLANT_SELECTED

        @staticmethod
        def bridge_selected_error(update: Update, _: CallbackContext) -> int:
            # error case of _conv_plant_status_bridge_selected step of Conversation started with '/status' command
            bridge_selected = update.message.text
            query_results = (PlantDataModel.query
                             .with_entities(PlantDataModel.bridge_id)
                             .distinct()
                             .order_by(PlantDataModel.bridge_id)
                             .all())
            reply_keyboard = get_keyboard_layout(list(chain(*query_results)))

            update.message.reply_markdown_v2(
                f'Sorry, I don\'t recognize any group named "{escape_markdown_V2(bridge_selected)}"\.\n'
                f'Please select again the group of plants you want to check the status of\.\n\n'
                f'Reply /cancel in any moment to end this conversation\.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )
            return PlantStatusCLS.States.BRIDGE_SELECTED

        @staticmethod
        def plant_selected(update: Update, _: CallbackContext) -> int:
            # continuation of Conversation started with '/status' command
            plant_selected = update.message.text
            regex_groups = re.search(PlantStatusCLS.REGEX, plant_selected)
            gateway_id = regex_groups.group('gateway')
            plant_name = regex_groups.group('name')

            report = get_plant_data_report(gateway_id, plant_name)

            # TODO prendi le piante dal model, e stampa un report specifico
            update.message.reply_markdown_v2(
                f'You selected the plant "{escape_markdown_V2(plant_selected)}"\.\n\n'
                f'{report}\n\n'
                f'That\'s all for now\! Hope to hear you soon\!\!',
                reply_markup=ReplyKeyboardRemove()
            )
            return PlantStatusCLS.States.END

        @staticmethod
        def plant_selected_error(update: Update, ctx: CallbackContext) -> int:
            # error case of _conv_plant_status_plant_selected step of Conversation started with '/status' command
            bridge_selected = ctx.user_data['bridge_selected']
            plant_selected = update.message.text
            query_results = (PlantDataModel.query
                             .join(PlantTypeModel)
                             .with_entities(PlantDataModel.gateway_id, PlantTypeModel.name)
                             .filter(PlantDataModel.bridge_id == bridge_selected)
                             .distinct()
                             .order_by(PlantTypeModel.name)
                             .all())
            keys = [f'{name} ({gtw_id})' for (gtw_id, name) in query_results]
            reply_keyboard = get_keyboard_layout(keys)

            update.message.reply_markdown_v2(
                f'Sorry, I don\'t recognize any plant named "{escape_markdown_V2(plant_selected)}"\.\n'
                f'Please select again the plant you want to check the status of, '
                f'or reply with /cancel to end the conversation\.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )
            return PlantStatusCLS.States.PLANT_SELECTED

        @staticmethod
        def fallback(update: Update, _: CallbackContext) -> int:
            update.message.reply_markdown_v2(f'Hope to hear you soon\!\!',
                                             reply_markup=ReplyKeyboardRemove())
            return PlantStatusCLS.States.END

    @property
    def handler(self) -> Handler:
        # noinspection PyTypeChecker
        return ConversationHandler(
            entry_points=[CommandHandler('plant_status', self.Callbacks.start)],
            states={
                self.States.BRIDGE_SELECTED: [
                    MessageHandler(FilterOnModelColumn(PlantDataModel, PlantDataModel.bridge_id),
                                   self.Callbacks.bridge_selected),
                    MessageHandler(Filters.text &
                                   ~Filters.command &
                                   ~FilterOnModelColumn(PlantDataModel, PlantDataModel.bridge_id),
                                   self.Callbacks.bridge_selected_error),
                ],
                self.States.PLANT_SELECTED: [
                    MessageHandler(FilterOnModelColumn(PlantDataModel, PlantDataModel.gateway_id,
                                                       self.REGEX, 'gateway'),
                                   self.Callbacks.plant_selected),
                    MessageHandler(Filters.text &
                                   ~Filters.command &
                                   ~FilterOnModelColumn(PlantDataModel, PlantDataModel.gateway_id,
                                                        self.REGEX, 'gateway'),
                                   self.Callbacks.plant_selected_error),
                ],
            },
            fallbacks=[CommandHandler('cancel', self.Callbacks.fallback)],
        )


Start = StartCLS()
Help = HelpCLS()
Echo = EchoCLS()
PlantStatusConversation = PlantStatusCLS()
