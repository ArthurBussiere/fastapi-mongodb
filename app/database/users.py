from database.database import Database
from models.users import User


class UsersCRUD(Database):
	def __init__(self):
		super().__init__(collection_name='users_collection')

	@staticmethod
	def document_helper(document) -> User:
		"""
		Converts a User document into a User model.
		"""
		return User(
			_id=str(document['_id']),
			username=document['username'],
			email=document['email'],
			role=document['role'],
			fullname=document.get('fullname'),
			disabled=document.get('disabled'),
			hashed_password=document.get('hashed_password'),
		)

	async def retrieve_all(self, query=None) -> list[User]:
		return await super().retrieve_all(query)

	async def retrieve_by_id(self, id) -> User:
		return await super().retrieve_by_id(id)

	async def insert(self, data) -> User:
		return await super().insert(data)

	async def update(self, id, data):
		return await super().update(id, data)

	async def delete_by_id(self, id):
		return await super().delete_by_id(id)

	# Additional item-specific methods can be added here if needed
	async def retrieve_a_user_by_username(self, username: str) -> User:
		"""
		Retrieve a user that match a given username.
		"""
		if document := await self.collection.find_one({'username': username}):
			return self.document_helper(document)


user_db = UsersCRUD()
