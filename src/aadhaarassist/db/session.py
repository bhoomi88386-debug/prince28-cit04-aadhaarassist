"""Database engine and session factory."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from aadhaarassist.config import Settings, get_settings
from aadhaarassist.db.url import to_asyncpg_url


def make_engine(settings: Settings):
    """Create an async SQLAlchemy engine using the supplied settings."""
    database_url = to_asyncpg_url(settings.database_url)

    return create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )


def make_sessionmaker(engine):
    """Create an async session factory for the supplied engine."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Default application engine, used by scripts such as db_check and load_db.
settings = get_settings()
engine = make_engine(settings)
SessionFactory = make_sessionmaker(engine)
