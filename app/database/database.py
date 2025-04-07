from abc import ABC, abstractmethod
from bson import ObjectId
from core.logger import logger
from core.config import settings
import motor.motor_asyncio


class Database(ABC):
	def __init__(
		self,
		collection_name: str,
		db_name: str = 'fastapi_mongodb',
		mongo_details: str = f'mongodb://{settings.MONGO_DB_USERNAME}:{settings.MONGO_DB_PASSWORD}@{settings.MONGO_DB_SERVER}',
	):
		"""
		Initialize the database connection.
		"""
		self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)
		self.database = self.client[db_name]
		self.collection = self.database[collection_name]
		self.logger = logger

	@staticmethod
	@abstractmethod
	def document_helper(document) -> dict:
		"""
		Converts a MongoDB document into a dictionary with specific fields.
		Must be implemented by subclasses.
		"""
		pass

	@abstractmethod
	async def retrieve_all(self, query=None, page_size: int = None, page_num: int = None) -> list:
		"""
		Retrieve all documents from the collection.
		"""
		documents = []
		cursor = self.collection.find(query)
		if page_size:
			cursor = cursor.skip(page_size * (page_num)).limit(page_size)
		total = await self.collection.count_documents({})
		async for document in cursor:
			documents.append(self.document_helper(document))
		return documents, total

	@abstractmethod
	async def retrieve_by_id(self, id: str) -> dict:
		"""
		Retrieve a single document by its ID.
		"""
		if document := await self.collection.find_one({'_id': ObjectId(id)}):
			return self.document_helper(document)

	@abstractmethod
	async def insert(self, data: dict):
		"""
		Insert a new document into the collection.
		"""
		result = await self.collection.insert_one(data)
		new_document = await self.collection.find_one({'_id': result.inserted_id})
		return self.document_helper(new_document)

	@abstractmethod
	async def update(self, id: str, data: dict):
		"""
		Insert an existing document into the collection.
		"""
		await self.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
		updated_document = await self.collection.find_one({'_id': ObjectId(id)})
		return self.document_helper(updated_document)

	@abstractmethod
	async def delete_by_id(self, id: str) -> dict:
		"""
		Delete a single document by its ID.
		"""
		deleted_document = await self.collection.find_one_and_delete({'_id': ObjectId(id)})
		return self.document_helper(deleted_document)
