from typing import Any

from pydantic import BaseModel
from typing import Generic, TypeVar


class ResponseModel(BaseModel):
    data: Any | None = None
    code: int
    message: str


# Define a generic type
T = TypeVar("T")


# Create a generic response model
class Response(BaseModel, Generic[T]):
    status: str
    total: int | None = None
    data: T | None = None
