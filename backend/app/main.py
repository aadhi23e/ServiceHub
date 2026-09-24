from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import (
    http_exception_handler,
    servicehub_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import ServiceHubError
from app.core.logging import configure_logging, logger

from app.middleware.request_id import RequestIDMiddleware
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)

    logger.info(
        "application_started",
        environment=settings.environment,
    )

    yield

    logger.info("application_stopped")


app = FastAPI(
    title="ServiceHub API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-CSRF-Token",
    ],
)
app.add_exception_handler(
    ServiceHubError,
    servicehub_exception_handler,
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)

app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "ServiceHub API",
        "version": "0.1.0",
    }
