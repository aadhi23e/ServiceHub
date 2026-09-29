# backend/app/schemas/user.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.servicehub import UserRole, UserStatus


class UserResponse(BaseModel):
    """
    Public representation of the authenticated user's account.
    Sensitive fields such as password_hash are never exposed.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None
    role: UserRole
    status: UserStatus
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(BaseModel):
    """
    Fields that an authenticated user is allowed to update.
    """

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=7, max_length=30)


class AdminUserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
