
from fastapi import Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.items import item_db
from models.items import ItemSchema
from models.response import ResponseModel



async def add_item(item: ItemSchema = Body(...)) -> ResponseModel:
    item = jsonable_encoder(item)
    new_item = await item_db.insert(item)
    return ResponseModel(data=new_item, message="Item added successfully", code=status.HTTP_201_CREATED)


async def get_items(name:str = None)-> ResponseModel:
    queries = {"name": name} if name else {}
    if items := await item_db.retrieve_all(queries):
        return ResponseModel(data=items, message="Items data retrieved successfully", code=status.HTTP_200_OK)
    return ResponseModel(data=[], message="No data retrieved", code=status.HTTP_200_OK)


async def get_item(id: str) -> ResponseModel:
    if item := await item_db.retrieve_by_id(id):
        return ResponseModel(data=item, message="Item data retrieved successfully", code=status.HTTP_200_OK)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item Not found")


async def delete_item(id: str) -> ResponseModel:
    if item := await item_db.retrieve_by_id(id):
        await item_db.delete_by_id(id)
        return ResponseModel(data=item, message="Item deleted successfully", code=status.HTTP_202_ACCEPTED)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item Not found")
