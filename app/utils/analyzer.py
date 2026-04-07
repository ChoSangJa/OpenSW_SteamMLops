from typing import List, Dict, Any

class Analyzer:
    GENRE_MAP = {
        # Action/Adventure
        570: "MOBA", 730: "FPS", 440: "FPS", 1172470: "Action RPG", 1245620: "Action RPG", 
        271590: "Open World", 1086940: "RPG", 1938090: "FPS", 236430: "Action",
        # Simulation/Strategy
        289070: "Strategy", 294100: "Simulation", 413150: "Casual", 250900: "Roguelike",
        883710: "Action", 646570: "Roguelike", 1145360: "Roguelike",
        # Indie/Casual
        105600: "Sandbox", 219740: "Action", 413150: "Farming Sim", 1794680: "Vampire-like",
        1158310: "Action RPG", 1446780: "Simulation"
    }

    def analyze_playstyle(self, games: List[Dict[str, Any]], achievements: Dict[int, Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a list of Steam games and achievement data to determine playstyle,
        preferred genres, and recommendations.
        """
        if not games:
            return {
                "total_playtime": 0.0,
                "playstyle": "No Public Games or Private Profile",
                "top_games": [],
                "recommendations": [],
                "genres": []
            }
            
        total_playtime_minutes = sum(game.get("playtime_forever", 0) for game in games)
        total_playtime_hours = round(total_playtime_minutes / 60, 2)
        
        # Genre Analysis
        genre_counts = {}
        for game in games:
            appid = game.get("appid")
            genre = self.GENRE_MAP.get(appid, "Other")
            if game.get("playtime_forever", 0) > 0:
                genre_counts[genre] = genre_counts.get(genre, 0) + game.get("playtime_forever", 0)
        
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        top_genres = [g[0] for g in sorted_genres[:3] if g[0] != "Other"]

        # Sort games by playtime descending
        sorted_games = sorted(games, key=lambda x: x.get("playtime_forever", 0), reverse=True)
        top_games = []
        for game in sorted_games[:5]:
            if game.get("playtime_forever", 0) == 0: continue
            
            appid = game.get("appid")
            ach_rate = 0.0
            if achievements and appid in achievements:
                ach_data = achievements[appid]
                if ach_data and "playerstats" in ach_data:
                    achs = ach_data["playerstats"].get("achievements", [])
                    if achs:
                        completed = sum(1 for a in achs if a.get("achieved") == 1)
                        ach_rate = round((completed / len(achs)) * 100, 1)
            
            top_games.append({
                "appid": appid,
                "name": game.get("name", "Unknown Game"),
                "playtime_hours": round(game.get("playtime_forever", 0) / 60, 2),
                "genre": self.GENRE_MAP.get(appid, "Game"),
                "achievement_rate": ach_rate
            })
        
        avg_ach_rate = sum(g["achievement_rate"] for g in top_games) / len(top_games) if top_games else 0
        playstyle = self._determine_playstyle(total_playtime_hours, len(games), avg_ach_rate)
        recommendations = self._get_recommendations(playstyle)
        
        return {
            "total_playtime": total_playtime_hours,
            "playstyle": playstyle,
            "top_games": top_games,
            "recommendations": recommendations,
            "genres": top_genres
        }
        
    def _determine_playstyle(self, hours: float, game_count: int, ach_rate: float = 0) -> str:
        if ach_rate > 80:
            return "The Completionist"
        
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

    def _get_recommendations(self, playstyle: str) -> List[Dict[str, str]]:
        rec_map = {
            "Hardcore Gamer": [
                {"name": "Elden Ring", "reason": "극한의 도전과 성취감을 선호하는 당신에게 추천합니다."},
                {"name": "Baldur's Gate 3", "reason": "깊이 있는 스토리와 몰입감을 선호하신다면 필수 게임입니다."},
                {"name": "Cyberpunk 2077", "reason": "고퀄리티 그래픽과 액션을 즐기기에 최적입니다."}
            ],
            "Dedicated Gamer": [
                {"name": "Hades", "reason": "반복되는 도전과 성장의 재미를 아시는 분께 추천합니다."},
                {"name": "Slay the Spire", "reason": "전략적인 플레이를 즐기는 당신에게 완벽한 선택입니다."},
                {"name": "Dave the Diver", "reason": "다양한 활동과 탐험을 즐기시는 취향에 적합합니다."}
            ],
            "Casual Gamer": [
                {"name": "Stardew Valley", "reason": "힐링과 평화로운 분위기를 좋아하신다면 추천합니다."},
                {"name": "Vampire Survivors", "reason": "간단하면서도 짜릿한 타격감을 느낄 수 있습니다."},
                {"name": "Among Us", "reason": "친구들과 가볍게 즐기기 좋은 심리 게임입니다."}
            ],
            "Occasional Gamer": [
                {"name": "Fall Guys", "reason": "가볍게 한두 판 즐기기에 부담 없는 게임입니다."},
                {"name": "PowerWash Simulator", "reason": "스트레스 해소와 평온함을 얻기 좋습니다."},
                {"name": "Portal 2", "reason": "짧고 강력한 퍼즐 경험을 선호하신다면 추천합니다."}
            ],
            "Collector (Buys but rarely plays)": [
                {"name": "Steam Summer Sale", "reason": "이미 많이 모으셨지만, 할인은 참을 수 없죠!"},
                {"name": "RimWorld", "reason": "라이브러리에 소장만 해도 든든한 명작입니다."}
            ]
        }
        return rec_map.get(playstyle, [{"name": "Skyrim", "reason": "언제나 좋은 선택입니다."}])
