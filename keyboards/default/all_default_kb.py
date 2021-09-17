from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sentiment_back_btn = KeyboardButton('Выбрать роль')
sentiment_back_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(sentiment_back_btn)

empty_kb = ReplyKeyboardMarkup()