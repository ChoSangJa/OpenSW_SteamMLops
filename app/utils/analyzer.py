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
        recommendations = self._get_recommendations(playstyle)
        
        return {
            "total_playtime": total_playtime_hours,
            "playstyle": playstyle,
            "top_games": top_games,
            "recommendations": recommendations
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
