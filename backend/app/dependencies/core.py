from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.core.redis import get_redis
from app.db.session import get_db

DBSession = Annotated[Session, Depends(get_db)]
RedisClient = Annotated[Redis, Depends(get_redis)]
