from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.user import UserRole, UserStatus


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None


class UserUpdateRequest(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )


class AdminUserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
