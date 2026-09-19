from enum import StrEnum


class Permission(StrEnum):
    PROFILE_READ_SELF = "profile.read_self"
    PROFILE_UPDATE_SELF = "profile.update_self"

    SERVICE_BROWSE = "service.browse"
    SERVICE_CREATE = "service.create"
    SERVICE_UPDATE_OWN = "service.update_own"
    SERVICE_DEACTIVATE_OWN = "service.deactivate_own"

    AVAILABILITY_MANAGE_OWN = "availability.manage_own"

    BOOKING_CREATE = "booking.create"
    BOOKING_READ_OWN = "booking.read_own"
    BOOKING_CANCEL_OWN = "booking.cancel_own"

    BOOKING_ACCEPT_OWN = "booking.accept_own"
    BOOKING_REJECT_OWN = "booking.reject_own"
    BOOKING_START_OWN = "booking.start_own"
    BOOKING_COMPLETE_OWN = "booking.complete_own"

    REVIEW_CREATE_OWN = "review.create_own"

    NOTIFICATION_READ_OWN = "notification.read_own"

    USER_READ = "user.read"
    USER_SUSPEND = "user.suspend"
    USER_ACTIVATE = "user.activate"

    PROVIDER_READ = "provider.read"

    BOOKING_READ_ALL = "booking.read_all"

    CATEGORY_MANAGE = "category.manage"

    AUDIT_READ = "audit.read"

    STATISTICS_READ = "statistics.read"