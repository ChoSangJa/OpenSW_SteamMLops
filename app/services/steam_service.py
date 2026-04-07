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
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
