from collections.abc import Callable
from typing import Annotated

from fastapi import Depends

from app.core.exceptions import AuthorizationError
from app.dependencies.auth import get_current_user
from app.enums.user import UserRole
from app.models.user import User


def require_roles(
    *allowed_roles: UserRole,
) -> Callable:

    def role_checker(
        current_user: Annotated[
            User,
            Depends(get_current_user),
        ],
    ) -> User:

        if current_user.status != "ACTIVE":
            raise AuthorizationError("Your account is not active.")

        allowed_values = {role.value for role in allowed_roles}

        if current_user.role not in allowed_values:
            raise AuthorizationError(
                "You do not have permission to perform this action."
            )

        return current_user

    return role_checker


require_customer = require_roles(
    UserRole.CUSTOMER,
)

require_provider = require_roles(
    UserRole.PROVIDER,
)

require_admin = require_roles(
    UserRole.ADMIN,
)

require_customer_or_provider = require_roles(
    UserRole.CUSTOMER,
    UserRole.PROVIDER,
)

require_provider_or_admin = require_roles(
    UserRole.PROVIDER,
    UserRole.ADMIN,
)
