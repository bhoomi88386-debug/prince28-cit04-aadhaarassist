"""Return API errors using RFC 9457 Problem Details."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def get_request_id(request: Request) -> str:
    """Get the request ID added by the middleware."""
    return getattr(request.state, "request_id", "unknown")


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Format HTTP errors as Problem Details."""
    title = "Not Found" if exc.status_code == 404 else "HTTP Error"

    body = {
        "type": "about:blank",
        "title": title,
        "status": exc.status_code,
        "detail": str(exc.detail),
        "instance": request.url.path,
        "request_id": get_request_id(request),
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=body,
        media_type="application/problem+json",
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Format validation errors as Problem Details."""
    errors = []

    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"])
        errors.append(
            {
                "field": location,
                "message": error["msg"],
            }
        )

    body = {
        "type": "about:blank",
        "title": "Unprocessable Content",
        "status": 422,
        "detail": "One or more request parameters are invalid.",
        "instance": request.url.path,
        "request_id": get_request_id(request),
        "errors": errors,
    }

    return JSONResponse(
        status_code=422,
        content=body,
        media_type="application/problem+json",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom API exception handlers."""
    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )


# Compatibility alias used by the app factory.
register_error_handlers = register_exception_handlers
