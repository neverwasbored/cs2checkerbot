import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .handlers import import_routers
from config import Config


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("aiogram").setLevel(logging.DEBUG)

dp = Dispatcher()


async def main():
    bot = Bot(token=Config.TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))

    await import_routers(dp=dp)
    print('Бот успешно запущен!')
    await dp.start_polling(bot)
