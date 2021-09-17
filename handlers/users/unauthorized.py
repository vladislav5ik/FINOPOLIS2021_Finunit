from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.all_inline_kb import role_kb
from data.config import admins
from loader import dp, bot
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.dispatcher.filters import Text
from states.all_states import States
from keyboards.default.all_default_kb import sentiment_back_kb


@dp.callback_query_handler(Text(startswith='role'),
                           state=States.UNAUTHORIZED_STATE)
async def process_test_sentiment_btn(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    role = int(callback_query.data[-1])
    await bot.edit_message_reply_markup(callback_query.from_user.id,
                                        callback_query.message.message_id)
    #if role == 1:
    #    await state.set_state(States.EMPLOYEE_CHOOSE_CHAT_STATE[0])
    #    await callback_query.message.answer("Вы выбрали роль сотрудник. Выберите чат чтобы начать работу:"
    #                                        , reply_markup=sentiment_back_kb)
    #if role == 2:
    #    await state.set_state(States.CUSTOMER_SETTINGS_STATE[0])
    #    await callback_query.message.answer("Вы выбрали роль клиент."
    #                                        , reply_markup=sentiment_back_kb)
    if role == 3:
        await state.set_state(States.TEST_SENTIMENT_STATE[0])

        await callback_query.message.answer("Отправьте любое сообщение, бот оценит его настроение:"
                                            , reply_markup=sentiment_back_kb)
