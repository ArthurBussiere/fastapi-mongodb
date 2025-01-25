from fastapi import Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.database.items import ItemDatabase

from app.models.items import (
    ItemSchema,
    UpdateItemSchema,
    ItemResponseModel
)

mongo_details = "mongodb://rootuser:rootpass@localhost:27017"

# Instantiate the ItemDatabase
item_db = ItemDatabase(mongo_details, "items")

async def add_item(item: ItemSchema = Body(...)) -> ItemResponseModel:
    item = jsonable_encoder(item)
    new_item = await item_db.insert(item)
    return ItemResponseModel(data=new_item, message="Item added successfully", code=status.HTTP_200_OK)


async def get_items(response: Response) -> ItemResponseModel:
    if items := await item_db.retrieve_all():
        return ItemResponseModel(data=items, message="Items data retrieved successfully", code=status.HTTP_200_OK)
    response.status_code = status.HTTP_204_NO_CONTENT
    return ItemResponseModel(data=items, message="Empty list returned", code=status.HTTP_204_NO_CONTENT)


async def get_item(id: str) -> ItemResponseModel:
    if item := await item_db.retrieve_by_id(id):
        return ItemResponseModel(data=item, message="Item data retrieved successfully", code=status.HTTP_200_OK)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item Not found")
