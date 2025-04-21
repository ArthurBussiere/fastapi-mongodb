from datetime import datetime, timedelta, timezone
from typing import Annotated
from passlib.context import CryptContext

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from models.auth import TokenData
from database.users import user_db
from models.users import User
from core.config import settings

from core.logger import logger

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
	return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	expire = datetime.now(timezone.utc)
	expire += expires_delta if expires_delta else timedelta(minutes=30)
	to_encode.update({'exp': expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
	to_encode.update({'exp': expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def authenticate_user(username: str, password: str) -> User:
	user = await user_db.retrieve_a_user_by_username(username)
	if not user:
		logger.error(f'Unknown user ({username}) try to authenticate')
		return False
	if not verify_password(password, user.hashed_password):
		logger.error(f'User ({username}) try to authenticate with an invalid password')
		return False
	return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'},
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		username: str = payload.get('sub')
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except Exception:
		raise credentials_exception
	user = await user_db.retrieve_a_user_by_username(username=token_data.username)
	if user is None:
		raise credentials_exception
	return user


async def get_current_active_user(
	current_user: Annotated[User, Depends(get_current_user)],
) -> User:
	if current_user.disabled:
		raise HTTPException(status_code=400, detail='Inactive user')
	return current_user


def conditional_auth_dependency(request: Request):
	client_host = request.client.host
	if client_host in ('127.0.0.1', 'localhost'):
		# Bypass auth for localhost
		return None
	# Otherwise run the real auth
	return get_current_active_user()
