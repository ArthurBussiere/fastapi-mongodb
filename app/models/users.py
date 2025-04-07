from enum import Enum
from pydantic import BaseModel, EmailStr, Field

from models.generic import PyObjectId


class UserRoleEnum(str, Enum):
    WATCHER = "watcher"
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRoleEnum
    fullname: str | None = None
    disabled: bool | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role: UserRoleEnum | None = None
    fullname: str | None = None
    disabled: bool | None = None


class User(UserBase):
    id: PyObjectId = Field(alias=("_id"))
    hashed_password: str
