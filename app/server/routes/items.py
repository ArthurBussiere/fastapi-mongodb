from fastapi import APIRouter, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_item, retrieve_items, add_item_data
)

from app.server.models.items import (
    ItemSchema,
    UpdateItemSchema,
    ItemResponseModel
)


async def add_item(item: ItemSchema = Body(...)) -> ItemResponseModel:
    item = jsonable_encoder(item)
    new_item = await add_item_data(item)
    return ItemResponseModel(data=new_item, message="Item added successfully", code=status.HTTP_200_OK)


async def get_items(response: Response) -> ItemResponseModel:
    if items := await retrieve_items():
        return ItemResponseModel(data=items, message="Items data retrieved successfully", code=status.HTTP_200_OK)
    response.status_code = status.HTTP_204_NO_CONTENT
    return ItemResponseModel(data=items, message="Empty list returned", code=status.HTTP_204_NO_CONTENT)


async def get_item(id: str) -> ItemResponseModel:
    if item := await retrieve_item(id):
        return ItemResponseModel(data=item, message="Item data retrieved successfully", code=status.HTTP_200_OK)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item Not found")
