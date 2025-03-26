from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_kb():
    keyboard = [
        [
            KeyboardButton(text='Get CS info')
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
