from fastapi import Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.database.users import UserDatabase

from app.models.users import UserSchema
from app.models.response import ResponseModel
from app.routes.generic import CRUDBase

class UserCRUD(CRUDBase[UserSchema, UserDatabase]):

    def __init__(self, db):
        super().__init__(db)

    async def add_user(user: UserSchema = Body(...)):
        return await user_crud.create(user)

    async def get_users(response: Response):
        return await user_crud.retrieve_all(response)

    async def get_user(id: str):
        return await user_crud.retrieve_by_id(id)

    async def delete_user(id: str):
        return await user_crud.delete(id)


# Instantiate the UserDatabase
mongo_details = "mongodb://rootuser:rootpass@localhost:27017"
user_db = UserDatabase(mongo_details, "users")
user_crud = UserCRUD(user_db)