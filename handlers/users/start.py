from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import admins
from loader import dp


@dp.message_handler(CommandStart())
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
    await message.answer(f'Привет, {message.from_user.full_name}!')
