import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import sqlmodel

SESSION_LIFETIME = timedelta(days=7)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _default_expiry() -> datetime:
    return _utcnow() + SESSION_LIFETIME


class Session(sqlmodel.SQLModel, table=True):

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    token: str = sqlmodel.Field(
        default_factory=lambda: uuid.uuid4().hex,
        unique=True,
        index=True,
        nullable=False,
    )
    user_id: int = sqlmodel.Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = sqlmodel.Field(default_factory=_utcnow, nullable=False)
    expires_at: datetime = sqlmodel.Field(default_factory=_default_expiry, nullable=False)