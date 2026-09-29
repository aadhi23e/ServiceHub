from fastapi import APIRouter

from app.api.v1.admin.organizations import router as organizations_router
from app.api.v1.admin.provider_approvals import (
    router as provider_approvals_router,
)

router = APIRouter()

router.include_router(organizations_router)
router.include_router(provider_approvals_router)

__all__ = ["organizations_router", "provider_approvals_router"]