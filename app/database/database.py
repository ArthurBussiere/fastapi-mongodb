import motor.motor_asyncio
from bson.objectid import ObjectId

# Parent Class for Database Operations
class Database:
    def __init__(self, mongo_details: str, db_name: str, collection_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    @staticmethod
    def document_helper(document) -> dict:
        """
        Converts a MongoDB document into a dictionary with a stringified ID.
        This can be overridden by child classes.
        """
        return {"id": str(document["_id"])}

    async def retrieve_all(self) -> list:
        """
        Retrieve all documents from the collection.
        """
        documents = []
        async for document in self.collection.find():
            documents.append(self.document_helper(document))
        return documents

    async def retrieve_by_id(self, id: str) -> dict:
        """
        Retrieve a single document by its ID.
        """
        if document := await self.collection.find_one({"_id": ObjectId(id)}):
            return self.document_helper(document)

    async def insert(self, data: dict) -> dict:
        """
        Insert a new document into the collection.
        """
        result = await self.collection.insert_one(data)
        new_document = await self.collection.find_one({"_id": result.inserted_id})
        return self.document_helper(new_document)


# Child Class for Item-Specific Operations
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