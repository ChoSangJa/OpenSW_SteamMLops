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
        print(f"Starting analysis for user: {steam_id}")
        # 1. Fetch steam data
        steam_service = SteamService()
        raw_data = await steam_service.get_owned_games(steam_id)
        
        if not raw_data or "response" not in raw_data:
            print(f"Analysis failed: Invalid response for {steam_id}")
            raise HTTPException(status_code=404, detail="Invalid response from Steam API")
            
        if "games" not in raw_data["response"]:
            print(f"Analysis failed: Private profile for {steam_id}")
            raise HTTPException(status_code=404, detail="No public games found, or profile is private")
            
        games = raw_data["response"]["games"]
        game_count = raw_data["response"].get("game_count", 0)
        print(f"Analyzing {len(games)} games for {steam_id}")
            
        # 2. Analyze data
        analyzer = Analyzer()
        analysis_result = analyzer.analyze_playstyle(games)
        
        print(f"Analysis complete for {steam_id}: {analysis_result['playstyle']}")
        # 3. Format response
        return AnalysisResponse(
            steam_id=steam_id,
            total_playtime_hours=analysis_result["total_playtime"],
            total_games_owned=game_count,
            playstyle=analysis_result["playstyle"],
            top_games=analysis_result["top_games"],
            recommendations=analysis_result["recommendations"]
        )
    except Exception as e:
        print(f"ERROR analyzing user {steam_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
