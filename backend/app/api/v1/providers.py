from fastapi import APIRouter, Depends

from app.core.rate_limit_dependencies import general_rate_limit


router = APIRouter(
    prefix="/providers",
    tags=["providers"],
    dependencies=[Depends(general_rate_limit)],
)