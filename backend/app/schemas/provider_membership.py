from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.provider import (
    AgentType,
    MembershipStatus,
    ProviderMembershipRole,
)


# Return a provider membership to the frontend.
class ProviderMembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organization_id: UUID
    role: ProviderMembershipRole
    agent_type: AgentType | None
    status: MembershipStatus
    invited_at: datetime | None
    joined_at: datetime | None
    removed_at: datetime | None


# Return a member together with basic user information.
class ProviderMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: ProviderMembershipRole
    agent_type: AgentType | None
    status: MembershipStatus
    invited_at: datetime | None
    joined_at: datetime | None


# Return all members of the authenticated provider organization.
class ProviderMemberListResponse(BaseModel):
    items: list[ProviderMemberResponse]


# Create an invitation for a new organization member.
class ProviderMemberInvitationCreate(BaseModel):
    email: EmailStr
    role: ProviderMembershipRole
    agent_type: AgentType | None = None


# Update an existing organization member.
class ProviderMembershipUpdate(BaseModel):
    role: ProviderMembershipRole | None = None
    agent_type: AgentType | None = None