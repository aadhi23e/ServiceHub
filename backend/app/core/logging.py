import logging
import sys

import structlog


def log_auth_event(
    event: str,
    *,
    user_id: int | None = None,
    success: bool | None = None,
) -> None:
    logger = structlog.get_logger("servicehub.auth")

    fields: dict[str, object] = {
        "event": event,
    }

    if user_id is not None:
        fields["user_id"] = user_id

    if success is not None:
        fields["success"] = success

    logger.info(
        event,
        **fields,
    )


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
        force=True,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()
