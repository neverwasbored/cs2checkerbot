from datetime import datetime

import aiohttp

from config import Config


class SteamApi:
    def __init__(self, steam_id: str | int):
        self.steam_api_key = Config.STEAM_API_KEY
        self.steam_id = steam_id

    async def get_steam_profile(self) -> tuple:
        if not self.steam_id:
            return False

        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.steam_api_key}&steamids={self.steam_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    return None

        player = data.get('response').get('players')[0]
        return player if player else None

    async def get_cs_stats(self) -> tuple:
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.steam_api_key}&steamid={self.steam_id}&include_appinfo=1&format=json"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    return None

        data_response = data.get('response')
        return data_response if data_response else None

    async def _validation(self) -> None:
        if await self._is_valid_steamid64(self.steam_id):
            return

        if isinstance(self.steam_id, str):
            vanity_name = self.steam_id.strip('/').split('/')[-1]
            self.steam_id = await self._convert_vanity_to_steam64(vanity_name=vanity_name)

            if self.steam_id:
                return True
            else:
                self.steam_id = None
                return False

    async def _is_valid_steamid64(self, steam_id: str | int) -> bool:
        """Проверяет, является ли ввод валидным SteamID64 (17-значное число)."""
        if isinstance(steam_id, int):
            return len(str(steam_id)) == 17

        if isinstance(steam_id, str):
            return steam_id.isdigit() and len(steam_id) == 17

        return False

    async def _convert_vanity_to_steam64(self, vanity_name: str) -> str | None:
        api_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={self.steam_api_key}&vanityurl={vanity_name}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()
                if data.get("response", {}).get("success") == 1:
                    return data["response"]["steamid"]
                else:
                    return None
