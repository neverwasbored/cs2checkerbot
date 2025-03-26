from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hlink

from utils.steam_api import SteamApi
from utils.faceit_api import FaceitApi
from ..states.steam_info import steam_state

router = Router()


@router.message(F.text == 'Get CS info')
async def enter_cs_id(message: Message, state: FSMContext):
    await message.answer(text='Напишите в чат SteamID пользователя или ссылку на профиль!')
    await state.set_state(steam_state.steam_id)


@router.message(StateFilter(steam_state.steam_id))
async def process_cs_info(message: Message, state: FSMContext):
    try:
        steam_id = message.text
        steam_api = SteamApi(steam_id=steam_id)

        # Валидация SteamID
        if not await steam_api._validation():
            await message.answer(
                text="❌ Ошибка!\n"
                     "Неверный SteamID или профиль скрыт.\n"
                     f"Проверьте {steam_id} и попробуйте снова."
            )
            await state.clear()
            return

        # Получение данных Steam
        steam_profile = await steam_api.get_steam_profile()
        if not steam_profile:
            await message.answer(
                text="❌ Профиль Steam не найден!\n"
                     f"SteamID: {steam_id}\n"
                     "Попробуйте позже."
            )
            await state.clear()
            return

        # Формирование ответа
        response = [
            "🎮 Профиль игрока",
            f"Steam Ник: {hbold(steam_profile.get('personaname'))}",
            f"SteamID64: {hbold(steam_profile.get('steamid'))}",
            f"Профиль: {hlink('ссылка', steam_profile.get('profileurl'))}",
            ""
        ]

        # Статистика игр
        game_stats = await steam_api.get_cs_stats()
        if game_stats:
            play_time = next(
                (game['playtime_forever'] // 60
                 for game in game_stats.get('games', [])
                 if game.get('appid') == 730
                 ), 0)

            response.extend([
                f"📊 Игровая статистика",
                f"Всего игр: {hbold(game_stats.get('game_count'))}",
                f"Часов в CS2: {hbold(play_time)}",
                ""
            ])

        # Faceit данные
        faceit_api = FaceitApi(steam_id=steam_profile.get('steamid'))
        faceit_account = await faceit_api.get_player_by_steam_id()

        if faceit_account:
            games = faceit_account.get('games', {})
            response.extend([
                "🏆 Faceit Профиль",
                f"Ник: {hbold(faceit_account.get('nickname'))}",
                f"Страна: {hbold(faceit_account.get('country'))}",
                f"CS2 ELO: {hbold(games.get('cs2', {}).get('faceit_elo', 'N/A'))}",
                f"CS:GO ELO: {hbold(games.get('csgo', {}).get('faceit_elo', 'N/A'))}",
                ""
            ])

            # Статистика Faceit
            faceit_stats = await faceit_api.get_player_stats(
                player_id=faceit_account.get('player_id')
            )
            if faceit_stats:
                response.extend([
                    "📈 Faceit Статистика",
                    f"Матчи: {hbold(faceit_stats.get('Matches'))}",
                    f"Win Rate: {hbold(faceit_stats.get('Win Rate %'))}%",
                    f"K/D: {hbold(faceit_stats.get('Average K/D Ratio'))}",
                    f"HS%: {hbold(faceit_stats.get('Average Headshots %'))}%"
                ])

        await message.answer(
            text="\n".join(response),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")
    finally:
        await state.clear()
