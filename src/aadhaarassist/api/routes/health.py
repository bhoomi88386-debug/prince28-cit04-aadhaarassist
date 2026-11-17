"""Health and readiness endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from aadhaarassist.api.deps import get_store
from aadhaarassist.store import DocumentStore

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    """Check whether the application is running."""
    return {"status": "ok"}


@router.get("/ready")
def ready(
    store: Annotated[DocumentStore, Depends(get_store)],
):
    """Check whether the application is ready to serve records."""
    if not store.is_loaded:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {"records_loaded": False},
            },
        )

    return {
        "status": "ok",
        "checks": {"records_loaded": True},
    }
