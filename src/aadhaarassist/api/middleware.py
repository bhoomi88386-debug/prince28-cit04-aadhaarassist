"""Middleware for request IDs and request logging."""

import logging
import time
import uuid

from starlette.requests import Request
from starlette.responses import Response

from aadhaarassist.logging_setup import request_id_ctx

logger = logging.getLogger("aadhaarassist")


async def request_context(request: Request, call_next) -> Response:
    """Add a request ID and log details for every HTTP request."""
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id
    context_token = request_id_ctx.set(request_id)

    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "HTTP request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
            },
        )

        request_id_ctx.reset(context_token)
