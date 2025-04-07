from database.database import Database
from models.items import Item


class ItemCRUD(Database):
	def __init__(self):
		super().__init__(collection_name='items_collection')

	@staticmethod
	def document_helper(document) -> Item:
		"""
		Converts an Item document into an ItemInDB model.
		"""
		return Item(id=str(document['_id']), name=document['name'], description=document['description'])

	async def retrieve_all(self, query=None) -> list[Item]:
		return await super().retrieve_all(query)

	async def retrieve_by_id(self, id) -> Item:
		return await super().retrieve_by_id(id)

	async def insert(self, data) -> Item:
		return await super().insert(data)

	async def update(self, id, data):
		return await super().update(id, data)

	async def delete_by_id(self, id):
		return await super().delete_by_id(id)

	# Additional item-specific methods can be added here if needed
	async def retrieve_by_name(self, name: str) -> list[Item]:
		"""
		Retrieve all items that match a given name.
		"""
		items = []
		async for item in self.collection.find({'name': name}):
			items.append(self.document_helper(item))
		return items


item_db = ItemCRUD()
