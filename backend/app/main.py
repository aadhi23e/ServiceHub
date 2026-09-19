# uvicorn app.main:app --reload

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging, logger
from app.middleware.request_id import RequestIDMiddleware


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

app.include_router(health_router)


@app.get("/")
def root():
    return {
        "name": "ServiceHub API",
        "version": "0.1.0",
    }