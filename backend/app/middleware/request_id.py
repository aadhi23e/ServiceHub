from uuid import uuid4

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


REQUEST_ID_HEADER = "X-Request-ID"


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        # --------------------------------------------------------
        # Request ID
        # --------------------------------------------------------
        request_id = (
            request.headers.get(REQUEST_ID_HEADER)
            or f"req_{uuid4().hex}"
        )

        # --------------------------------------------------------
        # Track ID
        # --------------------------------------------------------
        track_id = f"trk_{uuid4().hex}"

        # --------------------------------------------------------
        # Store on request.state
        # --------------------------------------------------------
        request.state.request_id = request_id
        request.state.track_id = track_id

        # --------------------------------------------------------
        # Bind to structlog context
        # --------------------------------------------------------
        structlog.contextvars.clear_contextvars()

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            track_id=track_id,
        )

        try:
            response = await call_next(request)

            # ----------------------------------------------------
            # Return correlation ID to client
            # ----------------------------------------------------
            response.headers[REQUEST_ID_HEADER] = request_id

            return response

        finally:
            # ----------------------------------------------------
            # Prevent context leaking into another request
            # ----------------------------------------------------
            structlog.contextvars.clear_contextvars()