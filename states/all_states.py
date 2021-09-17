from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(Helper):
    mode = HelperMode.snake_case

    UNAUTHORIZED_STATE = ListItem()
    TEST_SENTIMENT_STATE = ListItem()

    EMPLOYEE_CHATTING_STATE = ListItem()
    EMPLOYEE_CHOOSE_CHAT_STATE = ListItem()

    CUSTOMER_CREATE_CHAT_STATE = ListItem()
    CUSTOMER_CHATTING_STATE = ListItem()
    CUSTOMER_SETTINGS_STATE = ListItem()