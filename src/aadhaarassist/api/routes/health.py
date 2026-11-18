"""Health and readiness endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from aadhaarassist.db.session import engine

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Check whether the application is running."""
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    """Check whether the database is reachable."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {"database": False},
            },
        )

    return {
        "status": "ready",
        "checks": {"database": True},
    }
