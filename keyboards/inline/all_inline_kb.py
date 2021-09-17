from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, code, italic, text

role_kb = InlineKeyboardMarkup() \
    .row(InlineKeyboardButton('Сотрудник', callback_data='role1'),
         InlineKeyboardButton('Клиент', callback_data='role2'))
role_kb.add(InlineKeyboardButton('Проверить настроение сообщения', callback_data='role3'))


def sentiment_kb(percents):
    return InlineKeyboardMarkup()\
        .row(InlineKeyboardButton(emojize(f":grinning: {percents[0]}%"), callback_data='1'),
             InlineKeyboardButton(emojize(f":neutral_face: {percents[1]}%"), callback_data='2'),
             InlineKeyboardButton(emojize(f":rage: {percents[2]}%"), callback_data='3'))