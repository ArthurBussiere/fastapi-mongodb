from typing import Generic, TypeVar, Type
from fastapi import Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.models.response import ResponseModel

# Generic Type Variables
T = TypeVar("T")  # Model Schema Type
DB = TypeVar("DB")  # Database Type

class CRUDBase(Generic[T, DB]):
    def __init__(self, db: DB):
        self.db = db

    async def create(self, obj: T = Body(...)) -> ResponseModel:
        obj = jsonable_encoder(obj)
        new_obj = await self.db.insert(obj)
        return ResponseModel(data=new_obj, message="Added successfully", code=status.HTTP_200_OK)

    async def retrieve_all(self, response: Response) -> ResponseModel:
        if objects := await self.db.retrieve_all():
            return ResponseModel(data=objects, message="Data retrieved successfully", code=status.HTTP_200_OK)
        response.status_code = status.HTTP_204_NO_CONTENT
        return ResponseModel(data=[], message="Empty list returned", code=status.HTTP_204_NO_CONTENT)

    async def retrieve_by_id(self, id: str) -> ResponseModel:
        if obj := await self.db.retrieve_by_id(id):
            return ResponseModel(data=obj, message="Data retrieved successfully", code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    async def delete(self, id: str) -> ResponseModel:
        if obj := await self.db.retrieve_by_id(id):
            await self.db.delete_by_id(id)
            return ResponseModel(data=obj, message="Deleted successfully", code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")