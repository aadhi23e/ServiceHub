from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.core import DBSession
from app.services.booking_service import BookingService


def get_booking_service(
    db: DBSession,
) -> BookingService:
    return BookingService(db=db)


BookingServiceDependency = Annotated[
    BookingService,
    Depends(get_booking_service),
]