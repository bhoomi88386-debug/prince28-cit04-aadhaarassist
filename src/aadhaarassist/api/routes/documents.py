"""Endpoints for listing, searching, and retrieving documents."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from aadhaarassist.api.deps import get_repository
from aadhaarassist.db.repository import FILTER_KEY, DocumentRepository

router = APIRouter(prefix="/v1/documents", tags=["Documents"])


@router.get("")
async def list_documents(
    request: Request,
    repository: Annotated[DocumentRepository, Depends(get_repository)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    q: str | None = None,
):
    """List documents with optional search, metadata filters, and pagination."""
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
    }


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    repository: Annotated[DocumentRepository, Depends(get_repository)],
):
    """Retrieve one document by its ID."""
    document = await repository.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{document_id}'.",
        )

    return document
