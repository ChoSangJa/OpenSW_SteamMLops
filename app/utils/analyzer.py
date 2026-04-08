from typing import List, Dict, Any

class Analyzer:
    GENRE_MAP = {
        # Action/MOBA/FPS
        570: "MOBA", 730: "FPS", 440: "FPS", 1938090: "FPS", 1172470: "Battle Royale", 578080: "Battle Royale",
        236430: "Action", 883710: "Action",
        # RPG/Action RPG
        1086940: "RPG", 292030: "RPG", 378120: "Open World RPG", 1091500: "Open World RPG",
        1245620: "Action RPG", 814380: "Action RPG", 1158310: "Strategy", 1446780: "Action RPG", 582010: "Action RPG",
        # Open World/Sandbox
        271590: "Open World Action", 105600: "Sandbox Survival", 4000: "Sandbox Survival",
        # Strategy/Simulation/Management
        289070: "Strategy", 294100: "Simulation Management", 394360: "Strategy",
        # Indie/Casual/Roguelike
        413150: "Farming Sim", 250900: "Roguelike", 646570: "Roguelike", 1145360: "Roguelike",
        1794680: "Vampire-like", 219740: "Action Roguelike",
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
        top_genre = top_genres[0] if top_genres else None

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
        
        owned_game_names = {g.get("name", "").lower().strip() for g in games if g.get("name")}
        
        avg_ach_rate = sum(g["achievement_rate"] for g in top_games) / len(top_games) if top_games else 0
        playstyle = self._determine_playstyle(total_playtime_hours, len(games), avg_ach_rate, top_genre)
        recommendations = self._get_recommendations(total_playtime_hours, top_genre, owned_game_names)
        
        return {
            "total_playtime": total_playtime_hours,
            "playstyle": playstyle,
            "top_games": top_games,
            "recommendations": recommendations,
            "genres": top_genres
        }
        
    def _determine_playstyle(self, hours: float, game_count: int, ach_rate: float = 0, top_genre: str = None) -> str:
        base_style = ""
        genre_prefix = f"{top_genre} " if top_genre else ""
        
        if ach_rate > 80:
            return f"The {genre_prefix}Completionist"
        
        if hours > 2000:
            base_style = "Hardcore Gamer"
        elif hours > 500:
            base_style = "Dedicated Gamer"
        elif hours > 100:
            base_style = "Casual Gamer"
        elif hours > 0:
            base_style = "Occasional Gamer"
        else:
            return "Collector (Buys but rarely plays)"
            
        if top_genre:
            return f"{base_style} ({top_genre} Lover)"
        return base_style

    def _get_recommendations(self, hours: float, top_genre: str, owned_games: set) -> List[Dict[str, str]]:
        genre_recs = {
            "FPS": [
                {"name": "Valorant", "reason": "FPS 장르를 선호하시네요! 섬세한 에임과 전술이 요구되는 발로란트를 추천합니다."},
                {"name": "Apex Legends", "reason": "빠른 템포의 슈팅과 스킬 전투를 원하신다면 최고의 선택입니다."}
            ],
            "Battle Royale": [
                {"name": "Call of Duty: Warzone", "reason": "배틀로얄의 긴장감을 사랑하신다면 대규모 전장에 참전해보세요."},
                {"name": "Apex Legends", "reason": "속도감 넘치는 배틀로얄 경험을 선사합니다."}
            ],
            "RPG": [
                {"name": "The Witcher 3: Wild Hunt", "reason": "방대한 스토리와 깊이 있는 RPG를 사랑하신다면 필수입니다."},
                {"name": "Divinity: Original Sin 2", "reason": "최고의 턴제 RPG 경험을 선사합니다."}
            ],
            "Action RPG": [
                {"name": "Sekiro: Shadows Die Twice", "reason": "액션 RPG 팬이라면 짜릿한 패링의 쾌감을 느껴보세요."},
                {"name": "Monster Hunter: World", "reason": "거대한 몬스터를 사냥하는 수렵 액션의 정수입니다."}
            ],
            "Simulation Management": [
                {"name": "Factorio", "reason": "공장 경영과 시스템 자동화의 극한을 맛볼 수 있습니다."},
                {"name": "Cities: Skylines", "reason": "나만의 도시를 짓고 운영하는 최고의 시뮬레이션입니다."}
            ],
            "Strategy": [
                {"name": "Stellaris", "reason": "우주적 스케일의 대전략 게임을 좋아하실 것입니다."},
                {"name": "XCOM 2", "reason": "턴제 전략의 긴장감을 극대화한 명작입니다."}
            ],
            "Roguelike": [
                {"name": "Hades", "reason": "반복 플레이와 성장, 그리고 뛰어난 액션을 겸비했습니다."},
                {"name": "Dead Cells", "reason": "로그라이크와 메트로배니아의 완벽한 결합을 즐겨보세요."}
            ],
            "Farming Sim": [
                {"name": "My Time at Sandrock", "reason": "스타듀밸리 스타일의 여유로운 생활과 건설을 즐기실 수 있습니다."},
                {"name": "Coral Island", "reason": "아름다운 섬에서의 힐링 농장 게임입니다."}
            ],
            "Open World RPG": [
                {"name": "Red Dead Redemption 2", "reason": "역대 최고의 오픈월드 몰입감을 선사합니다."},
                {"name": "Horizon Zero Dawn", "reason": "아름다운 오픈월드와 독특한 세계관을 탐험해보세요."}
            ],
            "Open World Action": [
                {"name": "Batman: Arkham City", "reason": "시원한 액션과 훌륭한 오픈월드를 원한다면 추천합니다."}
            ],
            "MOBA": [
                {"name": "League of Legends", "reason": "MOBA 장르의 대명사, 치열한 협동 전투를 원하신다면 추천합니다."},
                {"name": "Smite", "reason": "3인칭 시점의 독특한 MOBA를 경험해보세요."}
            ]
        }
        
        fallback_recs = {
            "Hardcore": [
                {"name": "Elden Ring", "reason": "극한의 도전과 성취감을 즐기는 당신의 하드코어한 플레이 타임에 걸맞은 명작입니다."},
                {"name": "Baldur's Gate 3", "reason": "긴 플레이 타임을 몰입감 있게 보낼 수 있는 마스터피스입니다."}
            ],
            "Dedicated": [
                {"name": "Cyberpunk 2077", "reason": "어느 정도 진득하게 게임을 파고드는 성향이시군요, 방대한 나이트 시티로 떠나보세요."},
                {"name": "Terraria", "reason": "파고들 요소가 가득한 훌륭한 샌드박스입니다."}
            ],
            "Casual": [
                {"name": "Stardew Valley", "reason": "가볍게 힐링하며 즐기기에 완벽합니다."},
                {"name": "Dave the Diver", "reason": "캐주얼하지만 깊이 있는 다채로운 재미를 느끼기 좋습니다."}
            ]
        }

        recs = []
        if top_genre and top_genre in genre_recs:
            recs.extend(genre_recs[top_genre])
            
        # 플레이 타임에 따른 추가 추천
        if hours > 1000:
            recs.extend(fallback_recs["Hardcore"])
        elif hours > 300:
            recs.extend(fallback_recs["Dedicated"])
        elif hours > 0 and len(recs) < 3:
            recs.extend(fallback_recs["Casual"])
            
        # 고유한 게임 3개까지만 반환 (보유 중인 게임 제외)
        seen = set()
        final_recs = []
        for r in recs:
            rec_name_lower = r["name"].lower().strip()
            if rec_name_lower not in owned_games and r["name"] not in seen:
                seen.add(r["name"])
                final_recs.append(r)
                if len(final_recs) >= 3:
                    break
                    
        if not final_recs:
            if "the elder scrolls v: skyrim special edition" not in owned_games and "skyrim" not in owned_games:
                final_recs.append({"name": "Skyrim", "reason": "언제나 좋은 선택입니다."})
            elif "portal 2" not in owned_games:
                final_recs.append({"name": "Portal 2", "reason": "짧고 강력한 퍼즐 경험방식의 명작입니다."})
            else:
                final_recs.append({"name": "Hollow Knight", "reason": "훌륭한 레벨 디자인을 자랑하는 수작입니다."})
            
        return final_recs
