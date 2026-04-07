from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router

app = FastAPI(
    title="Steam User Analysis API",
    description="API for analyzing user playstyles based on Steam data",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
