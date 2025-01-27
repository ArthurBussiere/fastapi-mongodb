from enum import Enum
from pydantic import BaseModel


class UserRoleEnum(str, Enum):
    WATCHER = "watcher"
    USER = "user"
    ADMIN = "admin"


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    role: UserRoleEnum
    fullname: str | None = None
    disabled: bool | None = None



class UserInDB(BaseModel):
    id : str
    username: str
    email: str
    role: UserRoleEnum
    fullname: str | None = None
    disabled: bool | None = None
    hashed_password: str | None = None
