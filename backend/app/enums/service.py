from enum import StrEnum


class ServiceStatus(StrEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"


class ServiceMode(StrEnum):
    HOME_SERVICE = "HOME_SERVICE"
    AT_PROVIDER = "AT_PROVIDER"


class RequirementType(StrEnum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    SINGLE_SELECT = "SINGLE_SELECT"
    MULTI_SELECT = "MULTI_SELECT"
    FILE = "FILE"