from app.database.database import Database
from pydantic import BaseModel
from app.models.users import UserSchema

class UserDatabase(Database):
    def __init__(self, mongo_details: str, db_name: str):
        super().__init__(mongo_details, db_name, "users_collection")

    @staticmethod
    def document_helper(document) -> dict:
        """
        Converts an User document into a dictionary with specific fields.
        Overrides the parent method.
        """

        return {
            "id": str(document["_id"]),
            "username": document["username"],
            "email": document["email"],
            "fullname": document.get("fullname", None),
            "disabled": document.get("disabled", None),
        }
