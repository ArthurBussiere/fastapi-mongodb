from typing import Any, Optional

from pydantic import BaseModel

class ResponseModel(BaseModel):
    data: Optional[Any] = None
    code: int
    message: str

