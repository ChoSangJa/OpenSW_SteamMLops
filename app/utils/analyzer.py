from typing import List, Dict, Any

class Analyzer:
    def analyze_playstyle(self, games: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a list of Steam games to determine total playtime and top games,
        and assign a 'playstyle' tendency based on the metrics.
        """
        if not games:
            return {
                "total_playtime": 0.0,
                "playstyle": "No Public Games or Private Profile",
                "top_games": []
            }
            
        # Playtime is returned in minutes
        total_playtime_minutes = sum(game.get("playtime_forever", 0) for game in games)
        total_playtime_hours = round(total_playtime_minutes / 60, 2)
        
        # Sort games by playtime descending
        sorted_games = sorted(games, key=lambda x: x.get("playtime_forever", 0), reverse=True)
        top_games = [
            {
                "appid": game.get("appid"),
                "name": game.get("name", "Unknown Game"),
                "playtime_hours": round(game.get("playtime_forever", 0) / 60, 2)
            }
            for game in sorted_games[:5] if game.get("playtime_forever", 0) > 0
        ]
        
        playstyle = self._determine_playstyle(total_playtime_hours, len(games))
        
        return {
            "total_playtime": total_playtime_hours,
            "playstyle": playstyle,
            "top_games": top_games
        }
        
    def _determine_playstyle(self, hours: float, game_count: int) -> str:
        if hours > 2000:
            return "Hardcore Gamer"
        elif hours > 500:
            return "Dedicated Gamer"
        elif hours > 100:
            return "Casual Gamer"
        elif hours > 0:
            return "Occasional Gamer"
        else:
            return "Collector (Buys but rarely plays)"
