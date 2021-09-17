from requests import post
from aiogram import types
from .sentiment_classification import process_sentiment


def api_newchat_request(chat_name, chat_id):
    params = {'name': str(chat_name), 'id': str(chat_id)}
    response = post(f'https://pb-emotions.bubbleapps.io/version-test/api/1.1/wf/newchat'
                    , data=params)


def api_create_message_request(message, chat_id, sender, num_of_message, positive, neutral, negative):
    if sender == 'operator':
        emoji = 0
    params = {'message': message,
              'chat_id': chat_id,
              'sender': sender,
              'num_of_message': num_of_message,
              'positive': positive,
              'neutral': neutral,
              'negative': negative,
              'emoji': 0
              }
    response = post('https://pb-emotions.bubbleapps.io/version-test/api/1.1/wf/create_message', data=params)


def log_user_message(message: types.Message):
    positive, neutral, negative = process_sentiment(message.text)
    api_create_message_request(message=message.text,
                               chat_id=message.chat.id,
                               sender='client',
                               num_of_message=message.message_id,
                               positive=positive,
                               neutral=neutral,
                               negative=negative)


def log_bot_message(bot_text: str, message: types.Message):
    positive, neutral, negative = process_sentiment(message.text)
    api_create_message_request(message=bot_text,
                               chat_id=message.chat.id,
                               sender='operator',
                               num_of_message=message.message_id,
                               positive=positive,
                               neutral=neutral,
                               negative=negative)