from fastapi import Body, Response

from app.database.items import ItemDatabase

from app.models.items import ItemSchema
from app.routes.generic import CRUDBase

class ItemCRUD(CRUDBase[ItemSchema, ItemDatabase]):

    async def add_item(item: ItemSchema = Body(...)):
        return await item_crud.create(item)

    async def get_items(response: Response):
        return await item_crud.retrieve_all(response)

    async def get_item(id: str):
        return await item_crud.retrieve_by_id(id)

    async def delete_item(id: str):
        return await item_crud.delete(id)


# Instantiate the ItemDatabase
mongo_details = "mongodb://rootuser:rootpass@localhost:27017"
item_db = ItemDatabase(mongo_details, "items")
item_crud = ItemCRUD(item_db)