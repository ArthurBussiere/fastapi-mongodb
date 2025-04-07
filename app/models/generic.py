from typing import Annotated
from pydantic import AfterValidator, Field
from bson import ObjectId as _ObjectId


def check_object_id(value: str) -> str:
	if not _ObjectId.is_valid(value):
		raise ValueError('Invalid ObjectId')
	return value


PyObjectId = Annotated[str, AfterValidator(check_object_id), Field(pattern='^[0-9a-fA-F]{24}$')]
