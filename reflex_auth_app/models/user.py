from typing import Optional
import sqlmodel

class User(sqlmodel.SQLModel, table=True):
    # Modelo de usuario para autenticación

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    email: str = sqlmodel.Field(unique=True, index=True, nullable=False)
    password_hash:str = sqlmodel.Field(nullable=False)