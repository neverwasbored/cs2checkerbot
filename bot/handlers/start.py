from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards.main_keyboard import get_main_kb


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Привет: {message.from_user.username}!\nНажми на желаемую кнопку!', reply_markup=await get_main_kb())
