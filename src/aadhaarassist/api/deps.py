"""Shared dependencies used by API routes."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from aadhaarassist.db.repository import DocumentRepository
from aadhaarassist.db.session import SessionFactory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide one database session per request."""
    async with SessionFactory() as session:
        yield session


async def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentRepository:
    """Create a document repository using the request session."""
    return DocumentRepository(session)
