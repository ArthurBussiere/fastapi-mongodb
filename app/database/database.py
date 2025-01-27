from abc import ABC, abstractmethod
from core.config import settings
import motor.motor_asyncio


class Database(ABC):


    def __init__(
        self,
        db_name: str,
        collection_name: str,
        mongo_details: str = f"mongodb://{settings.MONGO_DB_USERNAME}:{settings.MONGO_DB_PASSWORD}@{settings.MONGO_DB_SERVER}"
    ):
        """
        Initialize the database connection.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    @staticmethod
    @abstractmethod
    def document_helper(document) -> dict:
        """
        Converts a MongoDB document into a dictionary with specific fields.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def retrieve_all(self, query=None) -> list:
        """
        Retrieve all documents from the collection.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def retrieve_by_id(self, id: str) -> dict:
        """
        Retrieve a single document by its ID.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def insert(self, data: dict) -> dict:
        """
        Insert a new document into the collection.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, id: str) -> dict:
        """
        Delete a single document by its ID.
        Must be implemented by subclasses.
        """
        pass
