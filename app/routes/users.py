from fastapi import Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.database.users import UserDatabase

from app.models.users import UserSchema
from app.models.response import ResponseModel

mongo_details = "mongodb://rootuser:rootpass@localhost:27017"

# Instantiate the UserDatabase
user_db = UserDatabase(mongo_details, "users")


async def add_user(user: UserSchema = Body(...)) -> ResponseModel:
    user = jsonable_encoder(user)
    new_user = await user_db.insert(user)
    return ResponseModel(data=new_user, message="User added successfully", code=status.HTTP_200_OK)


async def get_users(username: str = None, email: str = None) -> ResponseModel:
    queries = {"username": username} if username else {}
    queries.update({"email": email}) if email else None
    if users := await user_db.retrieve_all(queries):
        return ResponseModel(data=users, message="Users data retrieved successfully", code=status.HTTP_200_OK)
    return ResponseModel(data=users, message="Empty list returned", code=status.HTTP_200_OK)


async def get_user(id: str) -> ResponseModel:
    if user := await user_db.retrieve_by_id(id):
        return ResponseModel(data=user, message="User data retrieved successfully", code=status.HTTP_200_OK)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Not found")


async def delete_user(id: str) -> ResponseModel:
    if user := await user_db.retrieve_by_id(id):
        await user_db.delete_by_id(id)
        return ResponseModel(data=user, message="User deleted successfully", code=status.HTTP_200_OK)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Not found")