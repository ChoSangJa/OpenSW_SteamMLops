from pydantic import BaseModel
from typing import Dict, Any, List

class AnalysisResponse(BaseModel):
    steam_id: str
    total_playtime_hours: float
    total_games_owned: int
    playstyle: str
    top_games: List[Dict[str, Any]]
    recommendations: List[Dict[str, str]]
    genres: List[str]
