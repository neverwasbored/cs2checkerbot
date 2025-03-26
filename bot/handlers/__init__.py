from aiogram import Dispatcher

from .start import router as start_router
from .cs_info import router as steam_router


async def import_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(steam_router)
