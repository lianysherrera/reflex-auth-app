import uuid
from datetime import datetime, timezone
from typing import Optional

import sqlmodel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


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