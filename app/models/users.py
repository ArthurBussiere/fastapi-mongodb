from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRoleEnum(str, Enum):
    WATCHER = "watcher"
    USER = "user"
    ADMIN = "admin"


class UserSchema(BaseModel):
    username: str
    email: str
    role: UserRoleEnum
    fullname: str | None = None
    disabled: bool | None = None


class UserInDB(UserSchema):
    hashed_password: str
