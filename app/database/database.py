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

    async def delete_by_id(self, id: str) -> dict:
        """
        Delete a single document by its ID.
        """
        deleted_document =await self.collection.find_one_and_delete({"_id": ObjectId(id)})
        return self.document_helper(deleted_document)
