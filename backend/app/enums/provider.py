from enum import StrEnum


class ProviderStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class ProviderMembershipRole(StrEnum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    AGENT = "AGENT"


class MembershipStatus(StrEnum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REMOVED = "REMOVED"


class AgentType(StrEnum):
    MOBILE = "MOBILE"
    ON_SITE = "ON_SITE"
    HYBRID = "HYBRID"


class ProviderLocationType(StrEnum):
    SHOP = "SHOP"
    OFFICE = "OFFICE"
    SERVICE_CENTER = "SERVICE_CENTER"


class VerificationStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"