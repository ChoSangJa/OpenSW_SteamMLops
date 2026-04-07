# Steam User Analysis API Server (OpenSW_SteamMLops)

This project provides a FastAPI based web server to analyze a Steam user's playstyle based on their owned games and playtime.
It is built with MLOps considerations such as proper project structure, environment configuration, and containerization to make deploying it as part of an MLOps pipeline effortless.

## Architecture
- **FastAPI**: Provides a high-performance REST API.
- **Steam Web API**: Integrates with Steam to fetch `GetOwnedGames` data.
- **Pydantic**: Validates user configurations and API responses.
- **Docker**: Containerized for standard deployments across environments.

## Getting Started

### Prerequisites
- Python 3.11+
- Steam Web API Key (Get one from [here](https://steamcommunity.com/dev/apikey))

### Local Setup (Virtual Environment)
1. Navigate to the project root directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate it:
   - On Linux/macOS: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file from the example template: `cp .env.example .env`
6. Open `.env` and replace `your_steam_api_key_here` with your actual Steam Web API key.
7. Run the FastAPI server locally: 
   ```bash
   uvicorn app.main:app --reload
   ```
8. Access the automatically generated Swagger UI documentation at: `http://localhost:8000/docs`

### Docker Setup
To deploy using Docker:
1. Build the image: 
   ```bash
   docker build -t steam-analyzer .
   ```
2. Run the container (make sure your `.env` is configured): 
   ```bash
   docker run -p 8000:8000 --env-file .env steam-analyzer
   ```

## API Endpoints
- `GET /health` : Returns basic health check.
- `GET /api/v1/analyze/{steam_id}` : Returns user playstyle analysis.
  - *Note: `steam_id` format expects a 17 digit Steam64 ID (e.g. `76561197960434622`). The Steam account must be public to retrieve game data.*

