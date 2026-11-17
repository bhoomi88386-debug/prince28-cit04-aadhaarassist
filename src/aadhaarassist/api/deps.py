"""Shared dependencies used by API routes."""

from fastapi import Request

from aadhaarassist.store import DocumentStore


def get_store(request: Request) -> DocumentStore:
    """Return the document store attached to the application."""
    return request.app.state.store
