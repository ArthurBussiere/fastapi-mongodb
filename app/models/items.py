from typing import Any, Optional

from pydantic import BaseModel, Field

class ItemSchema(BaseModel):
    name: str = Field()
    description: str = Field()


class UpdateItemSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]


class ItemResponseModel(BaseModel):
    data: Optional[Any] = None
    code: int
    message: str

