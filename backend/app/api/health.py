from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health/live")
def liveness():
    return {
        "status": "ok",
    }