from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    PROVIDER = "PROVIDER" # orginization
    AGENT = "AGENT" # Orginization agent


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"
