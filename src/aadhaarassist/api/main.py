"""Create and configure the AadhaarAssist FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from aadhaarassist.api.errors import register_exception_handlers
from aadhaarassist.api.middleware import RequestLoggingMiddleware
from aadhaarassist.api.routes import documents, health
from aadhaarassist.config import Settings, get_settings
from aadhaarassist.db.session import engine
from aadhaarassist.logging_setup import setup_logging

logger = logging.getLogger("aadhaarassist")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the application with the supplied or environment settings."""
    settings = settings or get_settings()

    setup_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Starting AadhaarAssist with PostgreSQL")
        try:
            yield
        finally:
            await engine.dispose()
            logger.info("Database engine disposed")

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
