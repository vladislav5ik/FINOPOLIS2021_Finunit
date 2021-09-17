from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.users.api import log_bot_message, log_user_message, api_newchat_request
from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, code, italic, text
from loader import dp, bot
from .sentiment_classification import process_sentiment
from states.all_states import *
from keyboards.default.all_default_kb import sentiment_back_kb, empty_kb
from keyboards.inline.all_inline_kb import role_kb, sentiment_kb
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.all_inline_kb import role_kb
from data.config import admins
from loader import dp
from states.all_states import *



# await bot.send_audio(message.from_user.id, open("audio.mp3", "r"), performer = "Performer", title = "Title")
main_choice = ["интерактивный режим", "тестирование нейросети"]
styles = ["деловой", "обычный", "молодёжный"]
message_types = ["голосовые + текстовые", "только текстовые"]
sentiments = ["позитивный", "нейтральный", "отрицательный"]
sentiment_justification = {
        "позитивный":    "Представим что Вы задали вопрос в позитивном тоне.",
        "нейтральный":   "Представим что Вы задали вопрос в нейтраном тоне.",
        "отрицательный": "Представим что Вы задали вопрос в негативном тоне."
}

q_nested = {
"вклад":{
    "Узнать начисленные проценты": {
        "позитивный":    "Ваши начисленные проценты по карте ****ХХХХ составляют ZZZ рублей за Y месяцев. Хотели бы вы еще задать вопросы?",
        "нейтральный":   "Спасибо за вопрос! Ваши начисленные проценты по карте ****ХХХХ составляют ZZZ рублей за Y месяцев. Хотели бы вы еще задать вопросы? Мы с радостью ответим на них.",
        "отрицательный": "Спасибо за вопрос! Ваши начисленные проценты по карте ****ХХХХ составляют ZZZ рублей за Y месяцев. Наверянка, у вас есть еще вопросы, поэтому мы вас сейчас переведем на оператора. Подскажите, нужно ли это сделать? Хотели бы вы еще задать вопросы? Мы с радостью ответим на них."},
    "Узнать, как формируется вклад": {
        "позитивный":    "Вклад по вашей карте ****ХХХХ составляют формируются по условиям, которые представлены по ссылке: www.pochtabank.ru/xx Хотели бы вы еще задать вопросы?",
        "нейтральный":   "Спасибо за вопрос! Вклад по вашей карте ****ХХХХ составляют формируются по условиям, которые представлены по ссылке: www.pochtabank.ru/xx Хотели бы вы еще задать вопросы? Мы с радостью ответим на них.",
        "отрицательный": "Спасибо за вопрос! Вклад по вашей карте ****ХХХХ составляют формируются по условиям, которые представлены по ссылке: www.pochtabank.ru/xx . Наверняка, у вас есть еще вопросы, поэтому мы вас сейчас переведем на оператора. Подскажите, нужно ли это сделать?"},
    "Другой вопрос": {
        "позитивный":    "Перевести Вас на оператора?",
        "нейтральный":   "Перевести Вас на оператора?",
        "отрицательный": "Перевести Вас на оператора?"}},
"кредит": {
    "Узнать долг": {
        "позитивный":    "тут будет текст поз долг кредит",
        "нейтральный":   "тут будет текст нейтр долг кредит",
        "отрицательный": "тут будет текст отриц долг кредит"},
    "Узнать, как формируется кредит": {
        "позитивный":    "тут будет текст поз формир кредит",
        "нейтральный":   "тут будет текст нейтр формир кредит",
        "отрицательный": "тут будет текст отриц формир кредит"},
    "Другой вопрос": {
        "позитивный":    "Перевести Вас на оператора?",
        "нейтральный":   "Перевести Вас на оператора?",
        "отрицательный": "Перевести Вас на оператора?"}},
"другой вопрос": "Перевести Вас на оператора?"
}

yes_no = ['да, переключите меня на оператора', 'не нужно, мой вопрос решён']


class SetSettings(StatesGroup):
    test = State()
    main_choice = State()
    age = State()
    styles = State()
    message_types = State()
    sentiments = State()
    q_category = State()
    q_question = State()
    q_answer = State()
    operator = State()


@dp.message_handler(commands=['start'], state='*')
async def main_choice_start(message: types.Message):
    log_user_message(message)
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
        api_newchat_request(message.from_user.full_name, message.chat.id)
        with open("users.txt", "a") as file:
            file.write(user1 + "\n")
            file.close()
        for admin in admins:
            await message.bot.send_message(admin, f'New user - {message.from_user.username}')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in main_choice:
        keyboard.add(name)
    bot_text = "Выберите режим работы бота:"
    await message.answer(bot_text, reply_markup=keyboard)
    log_bot_message(bot_text, message)
    await SetSettings.main_choice.set()


@dp.message_handler(state=SetSettings.main_choice)
async def main_choice_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    choice = message.text.lower()
    if choice not in main_choice:
        bot_text = "Пожалуйста, выберите режим, используя клавиатуру ниже."
        await message.answer(bot_text)
        log_bot_message(bot_text, message)

        return
    await state.update_data(main_choice=message.text.lower())
    if choice == main_choice[1]:
        await SetSettings.test.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/start")
        bot_text = "Выбран тест-режим.\nВведите любое сообщение чтобы проверить его настроение."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        bot_text = 'нажмите кнопку /start чтобы вернуться к выбору режима'
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)
        return
    await SetSettings.age.set()
    bot_text = "Выбран интерактивный режим.\nПожалуйста, укажите ваш возраст:"
    await message.answer(bot_text, reply_markup=types.ReplyKeyboardRemove()); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.test)
async def bot_echo(message: types.Message):
    log_user_message(message)
    bot_text = 'Сообщение проанализировано'
    await message.reply(bot_text, reply_markup=sentiment_kb(process_sentiment(message.text)))
    log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.age)
async def age_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    if not message.text.isdigit():
        bot_text = "Пожалуйста, введите целое число."
        await message.answer(bot_text)
        log_bot_message(bot_text, message)

        return
    age = int(message.text)
    await state.update_data(age=age)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in ['да', 'другой']:
        keyboard.add(size)
    await SetSettings.styles.set()
    if age <= 25:
        bot_text = 'Хотите включить "молодёжный" стиль?'
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)
    elif age <= 35:
        bot_text = 'Хотите включить "обычный" стиль?'
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)
    else:
        bot_text = 'Хотите включить "деловой" стиль?'
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.styles)
async def style_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    msg = message.text.lower()
    if (msg not in styles) and (msg not in ['да', 'другой']):
        bot_text = "Пожалуйста, используйте клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return
    user_data = await state.get_data()
    age = user_data['age']
    if msg == 'другой':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if age <= 25:
            for size in ['обычный', 'деловой']:
                keyboard.add(size)
        elif age <= 35:
            for size in ['молодёжный', 'деловой']:
                keyboard.add(size)
        else:
            for size in ['молодёжный', 'обычный']:
                keyboard.add(size)
        bot_text = "Выберите другой стиль"
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)
        return

    if msg == 'да':
        if age <= 25:
            await state.update_data(style="молодёжный")
        elif age <= 35:
            await state.update_data(style="обычный")
        else:
            await state.update_data(style="деловой")
    else:
        await state.update_data(style=msg)
        await SetSettings.message_types.set()

    await SetSettings.message_types.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in message_types:
        keyboard.add(size)
    bot_text = "Хорошо. Теперь выберите тип сообщений"
    await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.message_types)
async def message_types_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    if message.text.lower() not in message_types:
        bot_text = "Пожалуйста, выберите тип сообщений, используя клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return
    await state.update_data(message_types=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in sentiments:
        keyboard.add(size)
    await SetSettings.sentiments.set()
    bot_text = "Пожалуйста, выберите настроение:"
    await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.sentiments)
async def sentiments_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    if message.text.lower() not in sentiments:
        bot_text = "Пожалуйста, выберите настроение, используя клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return
    await state.update_data(sentiments=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in q_nested.keys():
        keyboard.add(size)
    await SetSettings.q_category.set()
    bot_text = "Пожалуйста, выберите категорию вопроса:"
    await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.q_category)
async def q_category_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    if message.text not in q_nested.keys():
        bot_text = "Пожалуйста, выберите категорию вопроса, используя клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return
    q_category = message.text.lower()
    await state.update_data(q_category=q_category)
    user_data = await state.get_data()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if q_category == "другой вопрос":
        sentiment = user_data['sentiments']
        bot_text = "Оператор подключился, чтобы ответить на Ваш вопрос."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        await message.answer(sentiment_justification[sentiment])
        await SetSettings.main_choice.set()
        keyboard.add("/start")
        bot_text = "Спасибо за использование сервиса!\n" \
                   "Вы можете попробовать другие сценарии интерактивного режима с другим настроением"
        await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)
        return

    for size in q_nested[user_data['q_category']].keys():
        keyboard.add(size)
    await SetSettings.q_question.set()
    bot_text = "Выберите интересующий Вас вопрос"
    await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.q_question)
async def q_question_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    user_data = await state.get_data()
    q_question = message.text
    q_category = user_data['q_category']
    sentiment = user_data['sentiments']

    if q_question not in list(q_nested[q_category].keys()):
        bot_text = "Пожалуйста, интересующий Вас вопрос, используя клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return
    await state.update_data(q_question=q_question)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in yes_no:
        keyboard.add(size)
    await SetSettings.q_answer.set()
    bot_text = q_nested[q_category][q_question][sentiment]
    await message.answer(bot_text, reply_markup=keyboard); log_bot_message(bot_text, message)


@dp.message_handler(state=SetSettings.q_answer)
async def q_answer_chosen(message: types.Message, state: FSMContext):
    log_user_message(message)
    user_data = await state.get_data()
    sentiment = user_data['sentiments']
    q_category = user_data['q_category']
    q_question = user_data['q_category']
    q_answer = message.text
    if q_answer not in yes_no:
        bot_text = "Пожалуйста, используйте клавиатуру ниже."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        return


    if q_answer == yes_no[0]:
        sentiment = user_data['sentiments']
        bot_text = "Оператор подключился, чтобы ответить на Ваш вопрос."
        await message.answer(bot_text); log_bot_message(bot_text, message)
        bot_text = sentiment_justification[sentiment]
        await message.answer(bot_text); log_bot_message(bot_text, message)
    await SetSettings.main_choice.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    bot_text = "Спасибо за использование сервиса!\n"\
               "Вы можете попробовать другие сценарии интерактивного режима с другим настроением"
    await message.answer(bot_text, reply_markup=keyboard)


