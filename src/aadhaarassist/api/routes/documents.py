"""Endpoints for listing, searching, and retrieving documents."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from aadhaarassist.api.deps import get_store
from aadhaarassist.store import DocumentStore

router = APIRouter(prefix="/v1/documents", tags=["Documents"])


@router.get("")
def list_documents(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    q: str | None = None,
    store: Annotated[DocumentStore, Depends(get_store)] = None,
):
    """List documents with optional search and pagination."""
    items, total = store.list_documents(
        limit=limit,
        offset=offset,
        q=q,
    )

    return {
        "total": total,
        "items": items,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{document_id}")
def get_document(
    document_id: str,
    store: Annotated[DocumentStore, Depends(get_store)] = None,
):
    """Retrieve one document by its ID."""
    document = store.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{document_id}'.",
        )

    return document
