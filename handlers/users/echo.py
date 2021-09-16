from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, code, italic, text
from loader import dp
from .sentiment_classification import process_sentiment


@dp.message_handler()
async def bot_echo(message: types.Message):
    positive, neutral, negative = process_sentiment(message.text)
    await message.reply(text(emojize(f''':grinning:{positive}\n:neutral_face:{neutral}\n:rage:{negative}''')))
