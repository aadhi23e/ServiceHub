from fastapi import APIRouter

from app.api.v1.organizations.members import router as members_router
from app.api.v1.organizations.me import router as me_router
from app.api.v1.organizations.public import router as public_router

router = APIRouter()

router.include_router(members_router)
router.include_router(me_router)
router.include_router(public_router)
__all__ = ["me_router", "members_router", "public_router"]