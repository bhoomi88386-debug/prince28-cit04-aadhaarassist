"""Endpoints for listing, searching, and retrieving documents."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from aadhaarassist.api.deps import RepoDep
from aadhaarassist.db.repository import FILTER_KEY

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("")
async def list_documents(
    request: Request,
    repository: RepoDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    q: str | None = None,
):
    """List documents with optional search, filters, and pagination."""
    filters: dict[str, str] = {}

    for key, value in request.query_params.multi_items():
        if key in {"limit", "offset", "q"}:
            continue

        if not FILTER_KEY.fullmatch(key):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid filter name: '{key}'.",
            )

        filters[key] = value

    total, items = await repository.list(
        q=q,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    return {
        "total": total,
        "items": items,
        "limit": limit,
        "offset": offset,
        "filters": filters,
    }


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    repository: RepoDep,
):
    """Retrieve one document by its ID."""
    document = await repository.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{document_id}'.",
        )

    return document
