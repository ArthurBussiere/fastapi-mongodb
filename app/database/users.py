from app.database.database import Database
from app.models.users import UserInDB

class UserDatabase(Database):
    def __init__(self, mongo_details: str, db_name: str):
        super().__init__(mongo_details, db_name, "users_collection")

    @staticmethod
    def document_helper(document) -> UserInDB:
        """
        Converts an User document into a dictionary with specific fields.
        Overrides the parent method.
        """
        return UserInDB(
            id=str(document["_id"]),
            username=document["username"],
            email=document["email"],
            role=document["role"],
            fullname=document.get("fullname", None),
            disabled=document.get("disabled", None),
            hashed_password=document.get("hashed_password", None)
        )

    # Additional item-specific methods can be added here if needed
    async def retrieve_by_username(self, username: str) -> UserInDB:
        """
        Retrieve a user that match a given username.
        """
        if document := self.collection.find_one({"username": username}):
            return self.document_helper(document)
