from fastapi import APIRouter, Response, status

from app.core.health import check_dependencies

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/live")
def liveness() -> dict[str, str]:
    return {
        "status": "ok",
    }


@router.get("/ready")
def readiness(response: Response) -> dict[str, object]:
    dependencies = check_dependencies()

    if not dependencies.is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return {
            "status": "not_ready",
            "checks": {
                "postgres": dependencies.postgres,
                "redis": dependencies.redis,
            },
        }

    return {
        "status": "ready",
        "checks": {
            "postgres": True,
            "redis": True,
        },
    }
