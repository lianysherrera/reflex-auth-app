from datetime import datetime, timezone
from typing import Optional

import sqlmodel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Note(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    user_id: int = sqlmodel.Field(foreign_key="user.id", nullable=False, index=True)
    title: str = sqlmodel.Field(nullable=False)
    content: str = sqlmodel.Field(default="", nullable=False)
    created_at: datetime = sqlmodel.Field(default_factory=_utcnow, nullable=False)
