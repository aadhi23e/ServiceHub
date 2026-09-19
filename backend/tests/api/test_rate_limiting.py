from fastapi.testclient import TestClient

from app.main import app

client = TestClient(
    app,
    raise_server_exceptions=False,
)


# from app.api.v1.admin import router as admin_router
# from app.api.v1.bookings import router as bookings_router
# from app.api.v1.providers import router as providers_router
# from app.api.v1.services import router as services_router

# from app.core.rate_limit_dependencies import general_rate_limit


# def test_general_rate_limit_is_attached_to_resource_routers():
#     routers = [
#         providers_router,
#         services_router,
#         bookings_router,
#         admin_router,
#     ]

#     for router in routers:
#         dependency_functions = {
#             dependency.call
#             for dependency in router.dependencies
#         }

#         assert general_rate_limit in dependency_functions