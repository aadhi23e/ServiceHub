from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.user import router as user_router
# from app.api.v1.bookings import router as bookings_router
# from app.api.v1.providers import router as providers_router
# from app.api.v1.service_categories import router as services_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.provider import router as provider_router
from app.api.v1.service_categories import router as service_categories_router
from app.api.v1.services import router as services_router
from app.api.v1.provider_service_offerings import router as provider_service_offerings_router
from app.api.v1.organization_members import router as organization_router
from app.api.v1.provider_service_members import router as provider_service_members_router

v1_router = APIRouter(
    prefix="/v1",
)

v1_router.include_router(organizations_router)
v1_router.include_router(health_router)
v1_router.include_router(auth_router)
v1_router.include_router(admin_router)
v1_router.include_router(user_router)
v1_router.include_router(provider_router)
v1_router.include_router(service_categories_router)
v1_router.include_router(services_router)
v1_router.include_router(provider_service_offerings_router)
v1_router.include_router(organization_router)
v1_router.include_router(provider_service_members_router)
# v1_router.include_router(bookings_router)
# v1_router.include_router(providers_router)
# v1_router.include_router(services_router)
