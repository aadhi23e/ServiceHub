from enum import StrEnum


class UserRole(StrEnum):
    CUSTOMER = "CUSTOMER"
    PROVIDER = "PROVIDER"
    ADMIN = "ADMIN"

class RegistrationRole(StrEnum):
    CUSTOMER = "CUSTOMER"
    PROVIDER = "PROVIDER"
    

class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"
