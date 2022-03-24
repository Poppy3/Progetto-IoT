import re

from flask_sqlalchemy import Model
from sqlalchemy import Column
from telegram import Message
from telegram.ext import MessageFilter


class FilterOnModelColumn(MessageFilter):
    data_filter = True

    def __init__(self,
                 model: Model,
                 column: Column,
                 regex: str = None,
                 regex_group_as_filter: str = 'filter'):
        self.model: Model = model
        self.column: Column = column
        self.regex: str = regex
        self.regex_group_as_filter = regex_group_as_filter
        self.name = f'FilterOnModelColumn({self.model}, {self.column}, {self.regex}, {self.regex_group_as_filter})'

    def filter(self, message: Message):
        if message.text:
            if self.regex is None:
                col_filter = message.text
            else:
                try:
                    col_filter = re.search(self.regex, message.text).group(self.regex_group_as_filter)
                except (TypeError, AttributeError):
                    return False

            match = self.model.query.filter(self.column == col_filter).first()
            if match is not None:
                return True
        return False
