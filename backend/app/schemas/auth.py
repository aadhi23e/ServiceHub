from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.enums.user import UserRole, UserStatus


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

    role: UserRole = UserRole.CUSTOMER

    organization_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    legal_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    @model_validator(mode="after")
    def validate_registration(self) -> "RegisterRequest":
        if self.role == UserRole.ADMIN:
            raise ValueError(
                "Administrator accounts cannot be created through public registration."
            )

        if self.role == UserRole.PROVIDER and not self.organization_name:
            raise ValueError(
                "organization_name is required when registering as a provider."
            )

        if self.role == UserRole.CUSTOMER:
            if self.organization_name is not None:
                raise ValueError(
                    "organization_name is only allowed for provider registration."
                )

            if self.legal_name is not None:
                raise ValueError(
                    "legal_name is only allowed for provider registration."
                )

        return self


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None

    role: UserRole
    status: UserStatus


class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RegisterResponse(BaseModel):
    user: UserResponse