from fastapi import APIRouter

# from app.core.rate_limit_dependencies import general_rate_limit


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(general_rate_limit)],
)