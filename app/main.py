from datetime import datetime, timezone

from fastapi import FastAPI

from app.api.activity_routes import router as activity_router


app = FastAPI(title="Agenda Diaria API")
app.include_router(activity_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
