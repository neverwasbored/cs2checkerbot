import aiohttp

from config import Config


class FaceitApi:
    def __init__(self, steam_id: str | int):
        self.steam_id = steam_id
        self.headers = {
            'Authorization': Config.FACEIT_API_KEY
        }

    async def get_player_by_steam_id(self):
        url = f'https://open.faceit.com/data/v4/players?game=cs2&game_player_id={self.steam_id}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    return None
        return data

    async def get_player_stats(self, player_id: str):
        url = f'https://open.faceit.com/data/v4/players/{player_id}/stats/cs2'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    return None
        return data.get('lifetime')
