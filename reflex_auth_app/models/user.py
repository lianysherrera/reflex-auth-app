from typing import Optional
import sqlmodel

class User(sqlmodel.SQLModel, table=True):
    # Modelo de usuario para autenticación

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str = sqlmodel.Field(nullable=False)
    email: str = sqlmodel.Field(unique=True, index=True, nullable=False)
    password_hash: str = sqlmodel.Field(nullable=False)
    bio: Optional[str] = sqlmodel.Field(default=None, nullable=True)
    avatar_color: str = sqlmodel.Field(default="#4F46E5", nullable=False)