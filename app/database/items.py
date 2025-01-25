# Child Class for Item-Specific Operations
from app.database.database import Database


class ItemDatabase(Database):
    def __init__(self, mongo_details: str, db_name: str):
        # Initialize the parent class with the items collection
        super().__init__(mongo_details, db_name, "items_collection")

    @staticmethod
    def document_helper(document) -> dict:
        """
        Converts an Item document into a dictionary with specific fields.
        Overrides the parent method.
        """
        return {
            "id": str(document["_id"]),
            "name": document["name"],
            "description": document["description"],
        }

    # Additional item-specific methods can be added here if needed
    async def retrieve_by_name(self, name: str) -> list:
        """
        Retrieve all items that match a given name.
        """
        items = []
        async for item in self.collection.find({"name": name}):
            items.append(self.document_helper(item))
        return items