from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
<<<<<<< HEAD
# from app.api.v1.user import router as user_router
# from app.api.v1.bookings import router as bookings_router
# from app.api.v1.providers import router as providers_router
# from app.api.v1.service_categories import router as services_router
from app.api.v1.providers.organizations import (
    router as provider_organizations_router,
)
=======
from app.api.v1.user import router as user_router
# from app.api.v1.bookings import router as bookings_router
# from app.api.v1.providers import router as providers_router
# from app.api.v1.service_categories import router as services_router
>>>>>>> 879a53c08b0a052c2e7f2b51e7dfa3ddb394183b

v1_router = APIRouter(
    prefix="/v1",
)

v1_router.include_router(
    provider_organizations_router,
)
v1_router.include_router(health_router)
v1_router.include_router(auth_router)
<<<<<<< HEAD
# v1_router.include_router(user_router)
=======
v1_router.include_router(user_router)
>>>>>>> 879a53c08b0a052c2e7f2b51e7dfa3ddb394183b
# v1_router.include_router(bookings_router)
# v1_router.include_router(providers_router)
# v1_router.include_router(services_router)
