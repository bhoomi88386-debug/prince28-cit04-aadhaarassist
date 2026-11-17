"""Create and configure the AadhaarAssist FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from aadhaarassist.api.errors import register_exception_handlers
from aadhaarassist.api.middleware import RequestLoggingMiddleware
from aadhaarassist.api.routes import documents, health
from aadhaarassist.config import Settings, get_settings
from aadhaarassist.logging_setup import setup_logging
from aadhaarassist.store import DocumentStore

logger = logging.getLogger("aadhaarassist")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the application with the supplied or environment settings."""
    settings = settings or get_settings()

    setup_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        store = DocumentStore(settings.data_file)
        app.state.store = store

        try:
            count = store.load()
            logger.info(
                "Records loaded successfully",
                extra={"records": count},
            )
        except Exception:
            logger.exception("Could not load document records")

        yield

    app = FastAPI(
        title="AadhaarAssist",
        description="Aadhaar update assistance API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(health.router)
    app.include_router(documents.router)

    return app
