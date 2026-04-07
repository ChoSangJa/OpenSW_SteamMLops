from fastapi import APIRouter, HTTPException
import httpx
from app.services.steam_service import SteamService
from app.utils.analyzer import Analyzer
from app.models.schemas import AnalysisResponse

router = APIRouter()

@router.get("/analyze/{steam_id}", response_model=AnalysisResponse)
async def analyze_user(steam_id: str):
    """
    Given a Steam64 ID, fetch their game library and analyze their playstyle.
    Example valid steam_id: 76561198031548171
    """
    try:
        # 1. Fetch steam data
        steam_service = SteamService()
        raw_data = await steam_service.get_owned_games(steam_id)
        
        if not raw_data or "response" not in raw_data:
            raise HTTPException(status_code=404, detail="Invalid response from Steam API")
            
        if "games" not in raw_data["response"]:
            raise HTTPException(status_code=404, detail="No public games found, or profile is private")
            
        games = raw_data["response"]["games"]
        game_count = raw_data["response"].get("game_count", 0)
            
        # 2. Analyze data
        analyzer = Analyzer()
        analysis_result = analyzer.analyze_playstyle(games)
        
        # 3. Format response
        return AnalysisResponse(
            steam_id=steam_id,
            total_playtime_hours=analysis_result["total_playtime"],
            total_games_owned=game_count,
            playstyle=analysis_result["playstyle"],
            top_games=analysis_result["top_games"]
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Steam API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
