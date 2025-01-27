from database.database import Database
from models.items import ItemInDB

from database.database import Database
from models.items import ItemInDB
from bson.objectid import ObjectId


class ItemDatabase(Database):
    def __init__(self):
        super().__init__(db_name="items", collection_name="items_collection")

    @staticmethod
    def document_helper(document) -> ItemInDB:
        """
        Converts an Item document into an ItemInDB model.
        """
        return ItemInDB(
            id=str(document["_id"]),
            name=document["name"],
            description=document["description"]
        )


    async def retrieve_all(self, query=None) -> list[ItemInDB]:
        """
        Retrieve all items from the collection.
        """
        items = []
        async for document in self.collection.find(query):
            items.append(self.document_helper(document))
        return items

    async def retrieve_by_id(self, id: str) -> ItemInDB:
        """
        Retrieve a single item by its ID.
        """
        if document := await self.collection.find_one({"_id": ObjectId(id)}):
            return self.document_helper(document)


    async def insert(self, data: dict) -> ItemInDB:
        """
        Insert a new item into the collection.
        """
        result = await self.collection.insert_one(data)
        new_document = await self.collection.find_one({"_id": result.inserted_id})
        return self.document_helper(new_document)


    async def delete_by_id(self, id: str) -> ItemInDB:
        """
        Delete a single item by its ID.
        """
        deleted_document = await self.collection.find_one_and_delete({"_id": ObjectId(id)})
        return self.document_helper(deleted_document)


    # Additional item-specific methods can be added here if needed
    async def retrieve_by_name(self, name: str) -> list[ItemInDB]:
        """
        Retrieve all items that match a given name.
        """
        items = []
        async for item in self.collection.find({"name": name}):
            items.append(self.document_helper(item))
        return items


item_db = ItemDatabase()