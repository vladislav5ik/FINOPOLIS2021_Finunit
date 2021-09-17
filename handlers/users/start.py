from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.all_inline_kb import role_kb
from data.config import admins
from loader import dp
from states.all_states import *


async def bot_start(message: types.Message):
    user1 = ""
    exists = False
    with open("users.txt", "r") as user:
        use = user.readlines()
        for line in use:
            if line.strip() == str(message.from_user.id):
                exists = True
                user.close()
            else:
                user1 = str(message.from_user.id)
    if exists:
        print(f"user {message.from_user.id} already exists")
    else:
        print(f"New user - {message.from_user.id}")
        with open("users.txt", "a") as file:
            file.write(user1 + "\n")
            file.close()
        for admin in admins:
            await message.bot.send_message(admin, f'New user - {message.from_user.username}')
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.UNAUTHORIZED_STATE[0])
    await message.answer(f'Выберите роль, {message.from_user.full_name}!', reply_markup=role_kb)
