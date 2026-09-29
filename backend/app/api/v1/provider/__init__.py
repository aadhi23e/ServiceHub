from fastapi import APIRouter

from app.api.v1.provider.organization import router as provider_organization_router

router = APIRouter()

router.include_router(provider_organization_router)

__all__ = ["provider_organization_router"]