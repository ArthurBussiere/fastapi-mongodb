from app.database.database import Database
from app.models.items import ItemInDB

class ItemDatabase(Database):
    def __init__(self, mongo_details: str, db_name: str):
        super().__init__(mongo_details, db_name, "items_collection")

    @staticmethod
    def document_helper(document) -> ItemInDB:
        """
        Converts an Item document into a dictionary with specific fields.
        Overrides the parent method.
        """
        return ItemInDB(
            id=str(document["_id"]),
            name=document["name"],
            description=document["description"]
        )

    # Additional item-specific methods can be added here if needed
    async def retrieve_by_name(self, name: str) -> list[ItemInDB]:
        """
        Retrieve all items that match a given name.
        """
        items = []
        async for item in self.collection.find({"name": name}):
            items.append(self.document_helper(item))
        return items
