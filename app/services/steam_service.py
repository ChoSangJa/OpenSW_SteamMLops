import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

class SteamService:
    def __init__(self):
        self.api_key = settings.STEAM_API_KEY
        self.base_url = "http://api.steampowered.com"

    async def get_owned_games(self, steam_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch owned games for a given steam_id from the Steam Web API.
        Requires a valid STEAM_API_KEY.
        """
        if not self.api_key:
            raise ValueError("STEAM_API_KEY is not set in environment variables. Please check your .env file.")
            
        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "format": "json",
            "include_appinfo": "1",
            "include_played_free_games": "1"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"Fetching games for Steam ID: {steam_id}")
            response = await client.get(url, params=params)
            print(f"Steam API response status: {response.status_code}")
            response.raise_for_status()
            return response.json()

    async def get_player_achievements(self, steam_id: str, appid: int) -> Optional[Dict[str, Any]]:
        """
        Fetch player achievements for a specific game (appid).
        """
        url = f"{self.base_url}/ISteamUserStats/GetPlayerAchievements/v0001/"
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "appid": appid
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                # Note: This API sometimes returns 400 if the game has no achievements
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Warning: Failed to fetch achievements for appid {appid}: {e}")
            return None
