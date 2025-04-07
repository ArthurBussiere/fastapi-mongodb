from typing import List
from fastapi import Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.users import user_db

from models.users import UserCreate, UserUpdate, User
from models.response import Response

from components.authentication.auth_manager import get_password_hash


async def add_user(user: UserCreate = Body(...)) -> Response[User]:
	email = user.email
	existing_user, _ = await user_db.retrieve_all({'email': email})
	if existing_user:
		raise HTTPException(status.HTTP_409_CONFLICT, detail=f'User already exist with email: {email}')
	username = user.username
	existing_user, _ = await user_db.retrieve_all({'username': username})
	if existing_user:
		raise HTTPException(
			status.HTTP_409_CONFLICT,
			detail=f'User already exist with username: {username}',
		)
	user = jsonable_encoder(user)
	user['hashed_password'] = get_password_hash(user['password'])
	user.pop('password')
	new_user = await user_db.insert(user)
	return Response(status='User added successfully', data=new_user)


async def get_users(username: str = None, email: str = None) -> Response[List[User]]:
	queries = {'username': username} if username else {}
	queries.update({'email': email}) if email else None
	users, total = await user_db.retrieve_all(queries)
	return Response(data=users, total=total, status='Users data retrieved successfully')


async def get_user(id: str):
	if user := await user_db.retrieve_by_id(id):
		return Response(data=user, status='User data retrieved successfully')
	raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User Not found')


async def update_user(id: str, user: UserUpdate = Body(...)) -> Response[User]:
	user = jsonable_encoder(user, exclude_none=True)
	if user.get('password', None):
		user['hashed_password'] = get_password_hash(user['password'])
	user.pop('password', None)
	updated_user = await user_db.update(id, user)
	return Response(data=updated_user, status='User updated successfully')


async def delete_user(id: str) -> Response[User]:
	if user := await user_db.retrieve_by_id(id):
		await user_db.delete_by_id(id)
		return Response(data=user, status='User deleted successfully')
	raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User Not found')
