import os
import google.generativeai as genai
from typing import List
from app.core.config import settings

class LLMAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Using gemini-1.5-flash as it's fast and knowledgeable about gaming
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def analyze_genre(self, game_name: str, steam_tags: List[str]) -> str:
        """
        Takes the game name and the popular Steam community tags, 
        queries the LLM (which acts as a stand-in for an internet search synthesizer),
        and returns a highly specific, standardized genre classification.
        """
        if not self.model:
            # Fallback if no API key is provided
            return ", ".join(steam_tags) if steam_tags else "Game"

        tags_str = ", ".join(steam_tags) if steam_tags else "None"
        
        prompt = f"""
You are an expert video game categorizer and analyst.
You need to produce a concise, highly accurate, and specific genre classification for a game, combining Steam tags and internet consensus.

Game Name: {game_name}
Top Steam User Tags: {tags_str}

Please search your parametric internet knowledge for how this game is actually categorized by the gaming community and internet results.
Synthesize a single, descriptive genre string (e.g., "Souls-like Action RPG", "Metroidvania", "Asymmetric Multiplayer Horror", "Co-op Farming Sim").

Provide ONLY the genre string. Do not append any period or extra text.
"""
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            return tags_str
        except Exception as e:
            print(f"LLM API Error analyzing {game_name}: {e}")
            return ", ".join(steam_tags) if steam_tags else "Game"
