from database.database import Database
from models.users import UserInDB
from bson.objectid import ObjectId


class UserDatabase(Database):
    def __init__(self):
        super().__init__(db_name="users", collection_name="users_collection")


    @staticmethod
    def document_helper(document) -> UserInDB:
        """
        Converts a User document into a UserInDB model.
        """
        return UserInDB(
            id=str(document["_id"]),
            username=document["username"],
            email=document["email"],
            role=document["role"],
            fullname=document.get("fullname"),
            disabled=document.get("disabled"),
            hashed_password=document.get("hashed_password")
        )


    async def retrieve_all(self, query=None) -> list[UserInDB]:
        """
        Retrieve all users from the collection.
        """
        users = []
        async for document in self.collection.find(query):
            users.append(self.document_helper(document))
        return users


    async def retrieve_by_id(self, id: str) -> UserInDB:
        """
        Retrieve a single user by their ID.
        """
        if document := await self.collection.find_one({"_id": ObjectId(id)}):
            return self.document_helper(document)


    async def insert(self, data: dict) -> UserInDB:
        """
        Insert a new user into the collection.
        """
        result = await self.collection.insert_one(data)
        new_document = await self.collection.find_one({"_id": result.inserted_id})
        return self.document_helper(new_document)


    async def delete_by_id(self, id: str) -> UserInDB:
        """
        Delete a single user by their ID.
        """
        deleted_document = await self.collection.find_one_and_delete({"_id": ObjectId(id)})
        return self.document_helper(deleted_document)


    # Additional item-specific methods can be added here if needed
    async def retrieve_a_user_by_username(self, username: str) -> UserInDB:
        """
        Retrieve a user that match a given username.
        """
        if document := await self.collection.find_one({"username": username}):
            return self.document_helper(document)

user_db = UserDatabase()