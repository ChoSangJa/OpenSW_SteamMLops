import httpx
from typing import Dict, Any, Optional, List
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

    async def get_app_details(self, appid: int) -> Optional[Dict[str, Any]]:
        """
        Fetch store details for a specific game (appid), like genres.
        """
        url = "https://store.steampowered.com/api/appdetails"
        params = {
            "appids": appid,
            "l": "korean" # Return details in Korean mostly
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    str_appid = str(appid)
                    if data and str_appid in data and data[str_appid].get("success"):
                        return data[str_appid]["data"]
                return None
        except Exception as e:
            print(f"Warning: Failed to fetch app details for appid {appid}: {e}")
            return None

    async def get_storefront_tags(self, appid: int) -> List[str]:
        """
        Scrapes the Steam store page for the user tags, ignoring adult filters by cookie if necessary.
        Returns the top tags defined by the community.
        """
        from bs4 import BeautifulSoup
        
        url = f"https://store.steampowered.com/app/{appid}/"
        cookies = {
            'birthtime': '283993201', # Age bypass
            'lastagecheckage': '1-0-1980'
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0, cookies=cookies, headers=headers) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    return []
                soup = BeautifulSoup(response.text, "html.parser")
                tag_links = soup.select("a.app_tag")
                tags = []
                for t in tag_links:
                    tag_text = t.text.strip()
                    if tag_text != "+":
                        tags.append(tag_text)
                return tags[:5] # Return top 5 tags
        except Exception as e:
            print(f"Warning: Failed to fetch storefront tags for {appid}: {e}")
            return []
