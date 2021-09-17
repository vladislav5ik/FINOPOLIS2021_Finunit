#from aiogram import types
#from aiogram.utils.emoji import emojize
#from aiogram.utils.markdown import bold, code, italic, text
#from loader import dp, bot
#from .sentiment_classification import process_sentiment
#from states.all_states import *
#from keyboards.default.all_default_kb import sentiment_back_kb, empty_kb
#from keyboards.inline.all_inline_kb import role_kb, sentiment_kb
#
#@dp.message_handler(state=States.TEST_SENTIMENT_STATE)
#async def bot_echo(message: types.Message):
#    if message.text == 'Выбрать роль':
#        state = dp.current_state(user=message.from_user.id)
#        await state.set_state(States.UNAUTHORIZED_STATE[0])
#        await message.answer('Возвращение в главное меню', reply_markup=None)
#        await message.answer(f'Выберите роль, {message.from_user.full_name}!', reply_markup=role_kb)
#        return
#    await message.reply('Сообщение проанализировано', reply_markup=sentiment_kb(process_sentiment(message.text)))
    #positive, neutral, negative = process_sentiment(message.text)
    #await message.reply(text(emojize(f":grinning:{positive}%\n"
    #                                 f":neutral_face:{neutral}%\n"
    #                                 f":rage:{negative}%")), reply_markup=sentiment_back_kb)
